"""Mede quanto custa o passo de um subagente contra o da sessão principal.

Uso: python -I medir_subagentes.py <pasta de um projeto em ~/.claude/projects>

Não conta tokens por conta própria: chama o claude-context-cost (v1.6.3 ou
mais nova; pip install claude-context-cost) com --json na pasta. Ele soma as
sessões do projeto e os subagentes de cada uma (<sessão>/subagents/*.jsonl),
pelo uso da API gravado na transcrição. Daqui só saem as contagens, gravadas
em medidas.tsv (nesta pasta): nenhum nome de arquivo, id de sessão ou texto.

Passo = uma resposta do modelo; o custo do passo é o contexto que ela releu.
"""
import datetime
import json
import pathlib
import shutil
import statistics
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent


def rodar(pasta):
    """O --json do claude-context-cost para a pasta, já lido."""
    exe = shutil.which("claude-context-cost")
    if not exe:
        raise SystemExit("claude-context-cost não encontrado: pip install claude-context-cost")
    feito = subprocess.run([exe, "--json", str(pasta)], capture_output=True,
                           encoding="utf-8", check=False)
    if feito.returncode != 0:
        raise SystemExit(f"claude-context-cost saiu com {feito.returncode}: {feito.stderr.strip()}")
    return json.loads(feito.stdout)


def por_passo(linhas):
    """Tokens de contexto por resposta, de cada transcrição que respondeu."""
    return [l["total"] / l["responses"] for l in linhas if l["responses"]]


def peso_na_sessao(dados):
    """Parte dos subagentes no total de cada sessão que teve subagente, em %.

    Subagente cuja sessão não está na pasta (apagada) fica de fora: sem ela,
    o peso daria 100%.
    """
    sessoes = {t["file"]: t["total"] for t in dados["transcripts"]}
    dos_subagentes = {}
    for s in dados["subagents"]:
        dos_subagentes[s["session"]] = dos_subagentes.get(s["session"], 0) + s["total"]
    return [100 * sub / (sessoes[f"{sessao}.jsonl"] + sub)
            for sessao, sub in dos_subagentes.items()
            if sub and f"{sessao}.jsonl" in sessoes]


def resumo(dados):
    """As medidas, em ordem: (nome, valor)."""
    if "subagents" not in dados:
        raise SystemExit("o --json não tem subagentes: atualize o claude-context-cost (1.6.3 ou mais nova)")
    sessoes, subagentes = dados["transcripts"], dados["subagents"]
    if not por_passo(sessoes) or not por_passo(subagentes):
        raise SystemExit("a pasta precisa de sessões e de subagentes que responderam")
    passo_sessao = statistics.median(por_passo(sessoes))
    passo_sub = por_passo(subagentes)
    peso = peso_na_sessao(dados)
    if not peso:
        raise SystemExit("nenhum subagente com tokens numa sessão desta pasta")
    tokens_sub = sum(s["total"] for s in subagentes)
    return [
        ("versao_claude_context_cost", dados["version"]),
        ("respostas_projeto", dados["responses"]),
        ("tokens_projeto", dados["total"]),
        ("sessoes", len(sessoes)),
        ("respostas_sessoes", sum(t["responses"] for t in sessoes)),
        ("tokens_sessoes", sum(t["total"] for t in sessoes)),
        ("subagentes", len(subagentes)),
        ("sessoes_com_subagente", len({s["session"] for s in subagentes})),
        ("respostas_subagentes", sum(s["responses"] for s in subagentes)),
        ("tokens_subagentes", tokens_sub),
        ("subagentes_pct_do_projeto", f"{100 * tokens_sub / dados['total']:.1f}"),
        ("sessoes_com_resposta", len(por_passo(sessoes))),
        ("subagentes_com_resposta", len(passo_sub)),
        ("sessoes_no_peso", len(peso)),
        ("passo_sessao_mediana", round(passo_sessao)),
        ("passo_subagente_mediana", round(statistics.median(passo_sub))),
        ("passo_subagente_min", round(min(passo_sub))),
        ("passo_subagente_max", round(max(passo_sub))),
        ("razao_passo_subagente_sessao", f"{statistics.median(passo_sub) / passo_sessao:.2f}"),
        ("peso_subagentes_na_sessao_pct_min", f"{min(peso):.1f}"),
        ("peso_subagentes_na_sessao_pct_mediana", f"{statistics.median(peso):.1f}"),
        ("peso_subagentes_na_sessao_pct_max", f"{max(peso):.1f}"),
    ]


def tabela(medidas, quando):
    saida = ["medida\tvalor"] + [f"{nome}\t{valor}" for nome, valor in medidas]
    saida += ["", f"# medido em {quando}; passo = uma resposta; tokens = contexto relido"]
    return "\n".join(saida) + "\n"


def main(argv=None, destino=AQUI / "medidas.tsv", quando=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        raise SystemExit(__doc__)
    if quando is None:
        quando = datetime.date.today().strftime("%d/%m/%Y")
    texto = tabela(resumo(rodar(argv[0])), quando)
    pathlib.Path(destino).write_text(texto, encoding="utf-8")
    print(texto, end="")


if __name__ == "__main__":
    main()
