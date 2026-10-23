"""Pede ao Claude Code a descrição de um PR real e conta que arquivos ela cita.

Uso:
    python -I medir_pr.py rodar [rodadas]   (padrão: 5)
    python -I medir_pr.py contar

O PR é deste repositório: a branch pr-v0.5.0 (tag v0.5.0) contra a main em
v0.4.0. Cada rodada monta um clone novo numa pasta temporária (sem o remoto
e sem as tags, para a branch ser a única pista), roda uma vez

    claude -p "Escreva a descrição do pull request desta branch para a main"

no modelo padrão, só com git, Read, Grep e Glob, sem guardar a sessão, sem
os ganchos do usuário e sem o CLAUDE.md global (claudeMdExcludes), e grava a
descrição em rodadas/rodada-N.md e os números em rodadas/rodada-N.json.

"contar" lê as rodadas gravadas e classifica cada arquivo do
git diff --name-status: citado pelo caminho; pelo nome (só se o nome é único
no diff); ambíguo (o nome aparece, mas há outro igual no diff: conferir à
mão); só pela pasta; ou fora. Grava medidas.tsv (uma linha por rodada) e
arquivos.tsv (rodada × arquivo).
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
REPO = AQUI.parent
RODADAS = AQUI / "rodadas"
BASE, PONTA, BRANCH = "v0.4.0", "v0.5.0", "pr-v0.5.0"
FRASE = "Escreva a descrição do pull request desta branch para a main"
CATEGORIAS = ("caminho", "nome", "ambiguo", "pasta", "fora")


def git(pasta, *args):
    feito = subprocess.run(["git", "-C", os.fspath(pasta), *args], capture_output=True,
                           encoding="utf-8", check=False)
    if feito.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} saiu com {feito.returncode}: {feito.stderr.strip()}")
    return feito.stdout


def montar(destino):
    """Clone do repositório em destino: main em BASE, BRANCH em PONTA, sem remoto nem tags."""
    git(REPO, "clone", "--quiet", os.fspath(REPO), os.fspath(destino))
    git(destino, "checkout", "--quiet", "-b", BRANCH, PONTA)
    git(destino, "branch", "--quiet", "-f", "main", BASE)
    git(destino, "remote", "remove", "origin")
    tags = git(destino, "tag").split()
    if tags:
        git(destino, "tag", "-d", *tags)


def diff(pasta):
    """[(status, caminho)] do PR, na ordem do git."""
    linhas = git(pasta, "diff", "--name-status", f"main...{BRANCH}").splitlines()
    return [tuple(l.split("\t", 1)) for l in linhas if l]


def comando(exe):
    """A linha de comando de uma rodada."""
    global_md = (pathlib.Path.home() / ".claude" / "CLAUDE.md").as_posix()
    return [exe, "-p", FRASE, "--output-format", "json", "--no-session-persistence",
            "--setting-sources", "project,local",
            "--settings", json.dumps({"claudeMdExcludes": [global_md]}),
            "--tools", "Bash,Read,Grep,Glob",
            "--allowedTools", "Bash(git *),Read,Grep,Glob"]


def uma_rodada(exe, n):
    with tempfile.TemporaryDirectory(prefix="pr") as tmp:
        clone = pathlib.Path(tmp) / "ia-testada"
        montar(clone)
        feito = subprocess.run(comando(exe), cwd=clone, capture_output=True,
                               encoding="utf-8", check=False)
    if feito.returncode != 0:
        raise SystemExit(f"claude saiu com {feito.returncode} na rodada {n}: {feito.stderr.strip()}")
    dados = json.loads(feito.stdout)
    if dados.get("is_error"):
        raise SystemExit(f"a rodada {n} terminou em erro: {dados.get('subtype')}")
    RODADAS.mkdir(exist_ok=True)
    (RODADAS / f"rodada-{n}.md").write_text(dados["result"].strip() + "\n", encoding="utf-8")
    u = dados.get("usage", {})
    numeros = {
        "modelo": ",".join(sorted(dados.get("modelUsage", {}))),
        "turnos": dados.get("num_turns"),
        "duracao_s": round(dados.get("duration_ms", 0) / 1000, 1),
        "custo_usd": round(dados.get("total_cost_usd", 0), 4),
        "tokens_entrada": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                                     "cache_read_input_tokens")),
        "tokens_saida": u.get("output_tokens", 0),
        "quando": datetime.date.today().strftime("%d/%m/%Y"),
    }
    (RODADAS / f"rodada-{n}.json").write_text(json.dumps(numeros, ensure_ascii=False, indent=1) + "\n",
                                              encoding="utf-8")
    print(f"rodada {n}: {numeros}", flush=True)


def rodar(rodadas):
    exe = shutil.which("claude")
    if not exe:
        raise SystemExit("claude não encontrado no PATH")
    for n in range(1, rodadas + 1):
        uma_rodada(exe, n)


def aparece(trecho, texto):
    """trecho no texto, sem ser pedaço de outro caminho ou nome."""
    return re.search(r"(?<![\w./-])" + re.escape(trecho) + r"(?![\w/-])", texto) is not None


def classificar(caminho, texto, nomes):
    """Categoria de um arquivo do diff na descrição; nomes conta cada nome no diff."""
    if aparece(caminho, texto):
        return "caminho"
    nome = caminho.rsplit("/", 1)[-1]
    if "/" in caminho and aparece(nome, texto):
        return "nome" if nomes[nome] == 1 else "ambiguo"
    if "/" in caminho and aparece(caminho.split("/", 1)[0], texto):
        return "pasta"
    return "fora"


def conferencia(arquivo=AQUI / "conferencia.tsv"):
    """{(rodada, arquivo): categoria} da conferência à mão; vazio se não houver o arquivo."""
    if not pathlib.Path(arquivo).exists():
        return {}
    mao = {}
    for linha in pathlib.Path(arquivo).read_text(encoding="utf-8").splitlines()[1:]:
        if linha:
            rodada, caminho, categoria, _ = linha.split("\t", 3)
            if categoria not in CATEGORIAS:
                raise SystemExit(f"categoria desconhecida em conferencia.tsv: {categoria}")
            mao[(rodada, caminho)] = categoria
    return mao


def contar():
    with tempfile.TemporaryDirectory(prefix="pr") as tmp:
        clone = pathlib.Path(tmp) / "ia-testada"
        montar(clone)
        arquivos = diff(clone)
    nomes = {}
    for _, caminho in arquivos:
        nome = caminho.rsplit("/", 1)[-1]
        nomes[nome] = nomes.get(nome, 0) + 1
    rodadas = sorted(RODADAS.glob("rodada-*.md"), key=lambda p: int(p.stem.split("-")[1]))
    if not rodadas:
        raise SystemExit("nenhuma rodada gravada: rode antes 'medir_pr.py rodar'")
    mao = conferencia()
    medidas = ["rodada\tmodelo\tturnos\tduracao_s\tcusto_usd\ttokens_entrada\ttokens_saida\t"
               + "\t".join(CATEGORIAS) + "\tcorrigidos_a_mao"]
    detalhe = ["rodada\tstatus\tarquivo\tautomatica\tfinal"]
    for md in rodadas:
        n = md.stem.split("-")[1]
        texto = md.read_text(encoding="utf-8")
        num = json.loads(md.with_suffix(".json").read_text(encoding="utf-8"))
        cats = {c: 0 for c in CATEGORIAS}
        corrigidos = 0
        for status, caminho in arquivos:
            auto = classificar(caminho, texto, nomes)
            final = mao.pop((n, caminho), auto)
            corrigidos += final != auto
            cats[final] += 1
            detalhe.append(f"{n}\t{status}\t{caminho}\t{auto}\t{final}")
        medidas.append("\t".join(str(v) for v in (n, num["modelo"], num["turnos"], num["duracao_s"],
                                                  num["custo_usd"], num["tokens_entrada"],
                                                  num["tokens_saida"], *cats.values(), corrigidos)))
    if mao:
        raise SystemExit(f"conferencia.tsv cita arquivo ou rodada fora do diff: {sorted(mao)}")
    rodape = (f"\n# {len(arquivos)} arquivos no diff {BASE}...{PONTA}; categorias depois da "
              "conferência à mão (conferencia.tsv); ambiguo que sobrar = conferir\n")
    (AQUI / "medidas.tsv").write_text("\n".join(medidas) + "\n" + rodape, encoding="utf-8")
    (AQUI / "arquivos.tsv").write_text("\n".join(detalhe) + "\n", encoding="utf-8")
    print("\n".join(medidas) + "\n" + rodape, end="")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["rodar"] and len(argv) <= 2:
        rodar(int(argv[1]) if len(argv) == 2 else 5)
    elif argv == ["contar"]:
        contar()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
