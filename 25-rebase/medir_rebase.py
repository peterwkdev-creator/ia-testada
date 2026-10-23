"""Mostra, com git de verdade, quando um push forçado apaga o commit de um colega.

Uso: python -I medir_rebase.py

Sem IA e sem rede: cada cenário monta numa pasta temporária um remoto bare e
dois clones (você e o colega) da mesma branch feature. O colega empurra um
commit; você, sem saber, reescreve o seu (commit --amend, como num rebase) e
força o push de quatro jeitos:

1. --force
2. --force-with-lease
3. git fetch, depois --force-with-lease
4. git fetch, depois --force-with-lease --force-if-includes

Para cada um, grava em medidas.tsv (nesta pasta) se o push foi aceito e se o
commit do colega ainda está na feature do remoto. A configuração global e a
do sistema ficam de fora (GIT_CONFIG_GLOBAL e GIT_CONFIG_NOSYSTEM), para o
resultado não depender da máquina.
"""
import datetime
import os
import pathlib
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
CENARIOS = (
    ("force", False, ["--force"]),
    ("force_with_lease", False, ["--force-with-lease"]),
    ("fetch_e_force_with_lease", True, ["--force-with-lease"]),
    ("fetch_e_force_if_includes", True, ["--force-with-lease", "--force-if-includes"]),
)
AMBIENTE = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_DATE": "2026-10-23T12:00:00", "GIT_COMMITTER_DATE": "2026-10-23T12:00:00"}


def git(pasta, *args, pode_falhar=False):
    feito = subprocess.run(["git", "-C", os.fspath(pasta), "-c", "user.name=PKD",
                            "-c", "user.email=pkd@example.com", *args],
                           capture_output=True, encoding="utf-8", env=AMBIENTE, check=False)
    if feito.returncode != 0 and not pode_falhar:
        raise SystemExit(f"git {' '.join(args)} saiu com {feito.returncode}: {feito.stderr.strip()}")
    return feito


def commit(pasta, arquivo, texto, *extra):
    (pathlib.Path(pasta) / arquivo).write_text(texto, encoding="utf-8")
    git(pasta, "add", arquivo)
    git(pasta, "commit", "--quiet", "-m", texto, *extra)
    return git(pasta, "rev-parse", "HEAD").stdout.strip()


def cenario(tmp, buscar, opcoes):
    """(push aceito, commit do colega ainda na feature do remoto)."""
    tmp = pathlib.Path(tmp)
    remoto, voce, colega = tmp / "remoto.git", tmp / "voce", tmp / "colega"
    git(tmp, "init", "--quiet", "--bare", "--initial-branch=feature", os.fspath(remoto))
    git(tmp, "clone", "--quiet", os.fspath(remoto), os.fspath(voce))
    git(voce, "checkout", "--quiet", "-b", "feature")
    commit(voce, "base.txt", "base")
    commit(voce, "voce.txt", "seu commit")
    git(voce, "push", "--quiet", "origin", "feature")
    git(tmp, "clone", "--quiet", "--branch", "feature", os.fspath(remoto), os.fspath(colega))
    do_colega = commit(colega, "colega.txt", "commit do colega")
    git(colega, "push", "--quiet", "origin", "feature")
    commit(voce, "voce.txt", "seu commit, reescrito", "--amend")
    if buscar:
        git(voce, "fetch", "--quiet", "origin")
    aceito = git(voce, "push", "--quiet", *opcoes, "origin", "feature", pode_falhar=True).returncode == 0
    ficou = git(remoto, "merge-base", "--is-ancestor", do_colega, "feature",
                pode_falhar=True).returncode == 0
    return aceito, ficou


def medir():
    linhas = []
    for nome, buscar, opcoes in CENARIOS:
        with tempfile.TemporaryDirectory(prefix="rb") as tmp:
            aceito, ficou = cenario(tmp, buscar, opcoes)
        linhas.append((nome, " ".join(opcoes), "sim" if buscar else "não",
                       "aceito" if aceito else "barrado", "sim" if ficou else "não"))
    return linhas


def tabela(linhas, versao, quando):
    saida = ["cenario\topcoes\tfetch_antes\tpush\tcommit_do_colega_no_remoto"]
    saida += ["\t".join(l) for l in linhas]
    saida += ["", f"# medido em {quando} com {versao}"]
    return "\n".join(saida) + "\n"


def main(argv=None, destino=AQUI / "medidas.tsv", quando=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        raise SystemExit(__doc__)
    if quando is None:
        quando = datetime.date.today().strftime("%d/%m/%Y")
    versao = git(AQUI, "--version").stdout.strip()
    texto = tabela(medir(), versao, quando)
    pathlib.Path(destino).write_text(texto, encoding="utf-8")
    print(texto, end="")


if __name__ == "__main__":
    main()
