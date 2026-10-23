"""Compara o custo de uma tarefa feita por uma sessão só e por um agent team.

Uso: python -I medir_time.py <pasta do projeto solo> <pasta do projeto do time>

As duas pastas ficam em ~/.claude/projects (uma por projeto). Não conta
tokens por conta própria: chama o claude-context-cost (v1.6.3 ou mais nova;
pip install claude-context-cost) com --json em cada pasta. No time, a sessão
é o líder e os teammates aparecem como subagentes
(<sessão do líder>/subagents/*.jsonl). Daqui só saem as contagens, gravadas
em medidas.tsv (nesta pasta), com o nome que a tarefa deu a cada teammate:
nenhum nome de arquivo, id de sessão ou texto.

No Windows, o caminho de um teammate passa fácil dos 260 caracteres e o
claude-context-cost 1.6.4 falha (WinError 3); por isso cada pasta é copiada
antes para uma pasta temporária de caminho curto.
"""
import datetime
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent


def longo(caminho):
    """O caminho com o prefixo que libera os 260 caracteres no Windows.

    Fora do Windows, ou se o prefixo já está, o caminho volta como veio.
    """
    caminho = os.fspath(caminho)
    if os.name != "nt" or caminho.startswith("\\\\?\\"):
        return caminho
    return "\\\\?\\" + os.path.abspath(caminho)


def rodar(pasta):
    """O --json do claude-context-cost para a pasta, já lido, de uma cópia curta."""
    exe = shutil.which("claude-context-cost")
    if not exe:
        raise SystemExit("claude-context-cost não encontrado: pip install claude-context-cost")
    if not pathlib.Path(pasta).is_dir():
        raise SystemExit(f"pasta não encontrada: {pasta}")
    with tempfile.TemporaryDirectory(prefix="at") as tmp:
        copia = os.path.join(tmp, "p")
        shutil.copytree(longo(pasta), longo(copia))
        feito = subprocess.run([exe, "--json", copia], capture_output=True,
                               encoding="utf-8", check=False)
    if feito.returncode != 0:
        raise SystemExit(f"claude-context-cost saiu com {feito.returncode}: {feito.stderr.strip()}")
    return json.loads(feito.stdout)


def somas(linhas):
    """(transcrições, respostas, tokens) das linhas do --json."""
    return len(linhas), sum(l["responses"] for l in linhas), sum(l["total"] for l in linhas)


def nome_teammate(arquivo):
    """O nome dado ao teammate na tarefa: agent-a<nome>-<id>.jsonl vira <nome>."""
    m = re.fullmatch(r"agent-a(.+)-[0-9a-f]+\.jsonl", arquivo)
    if not m:
        raise SystemExit("teammate fora do padrão agent-a<nome>-<id>.jsonl")
    return m.group(1)


def resumo(solo, time):
    """As medidas, em ordem: (nome, valor)."""
    for nome, dados in (("solo", solo), ("time", time)):
        if "subagents" not in dados:
            raise SystemExit("o --json não tem subagentes: atualize o claude-context-cost (1.6.3 ou mais nova)")
        if not dados["total"]:
            raise SystemExit(f"a pasta do {nome} não tem tokens")
    if solo["subagents"]:
        raise SystemExit("a pasta do solo tem subagentes: a comparação pede uma sessão só")
    teammates = [s for s in time["subagents"] if s["responses"]]
    if not teammates:
        raise SystemExit("a pasta do time não tem teammates que responderam")
    _, resp_lider, tok_lider = somas(time["transcripts"])
    n_tm, resp_tm, tok_tm = somas(teammates)
    if solo["version"] != time["version"]:
        raise SystemExit("as duas pastas foram medidas com versões diferentes do claude-context-cost")
    return [
        ("versao_claude_context_cost", solo["version"]),
        ("solo_sessoes", len(solo["transcripts"])),
        ("solo_respostas", solo["responses"]),
        ("solo_tokens", solo["total"]),
        ("time_sessoes_lider", len(time["transcripts"])),
        ("time_lider_respostas", resp_lider),
        ("time_lider_tokens", tok_lider),
        ("time_teammates", n_tm),
        ("time_teammates_respostas", resp_tm),
        ("time_teammates_tokens", tok_tm),
    ] + [
        (f"teammate_{nome}_{campo}", valor)
        for nome, s in sorted((nome_teammate(s["file"]), s) for s in teammates)
        for campo, valor in (("respostas", s["responses"]), ("tokens", s["total"]))
    ] + [
        ("time_respostas", time["responses"]),
        ("time_tokens", time["total"]),
        ("contextos_no_time", 1 + n_tm),
        ("razao_time_solo", f"{time['total'] / solo['total']:.1f}"),
    ]


def tabela(medidas, quando):
    saida = ["medida\tvalor"] + [f"{nome}\t{valor}" for nome, valor in medidas]
    saida += ["", f"# medido em {quando}; tokens = contexto relido, somado nas respostas"]
    return "\n".join(saida) + "\n"


def main(argv=None, destino=AQUI / "medidas.tsv", quando=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        raise SystemExit(__doc__)
    if quando is None:
        quando = datetime.date.today().strftime("%d/%m/%Y")
    texto = tabela(resumo(rodar(argv[0]), rodar(argv[1])), quando)
    pathlib.Path(destino).write_text(texto, encoding="utf-8")
    print(texto, end="")


if __name__ == "__main__":
    main()
