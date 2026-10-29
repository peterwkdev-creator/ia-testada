"""Pede ao Claude Code os testes de unidade de um módulo e conta quantos defeitos plantados eles pegam.

Uso:
    python -I medir_teste_verde.py rodar [rodadas] [A|B|C]   (padrão: 5, as três condições)
    python -I medir_teste_verde.py contar

O módulo é projeto/carrinho.py. Cada rodada copia SÓ a pasta projeto/ para
uma pasta temporária nova (os defeitos e a referência nunca entram lá) e roda
uma vez, no modelo padrão,

    claude -p "<frase da condição>"

com Read, Write, Edit, Glob, Grep e Bash liberado só para python, sem
guardar a sessão, sem os ganchos do usuário e sem o CLAUDE.md global
(claudeMdExcludes). A condição A pede os testes; a B pede os testes e a
prova de que pegam defeito. O test_carrinho.py gerado vai para
rodadas/<condição>-<n>/ e os números (modelo, turnos, duração, custo,
tokens; nenhum texto da sessão) para rodadas/<condição>-<n>/numeros.json.
Rodada já gravada não se refaz: para refazer, apague a pasta dela.

"contar" roda cada suíte gravada no carrinho.py certo e em cada um dos
defeitos/*.py (o certo com uma linha trocada). Pegou = algum teste falha ou
dá erro. Suíte que não fica verde no certo conta à parte (não vale como
"pegou"). Grava medidas.tsv (uma linha por rodada, com o resumo por condição
no rodapé) e defeitos.tsv (rodada × defeito).

Condição C: a frase da A sobre projeto-c/carrinho.py, o mesmo código com as
docstrings sem os exemplos de fronteira (sem_docstrings confere que o código
é igual), contada contra defeitos-c/ (os mesmos 10 defeitos nesse arquivo).
"""
import ast
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import statistics
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
PROJETO = AQUI / "projeto"
CARRINHO = PROJETO / "carrinho.py"
DEFEITOS = AQUI / "defeitos"
# C: o mesmo código, com as docstrings sem os exemplos de fronteira, e os mesmos 10 defeitos nele
PROJETO_C = AQUI / "projeto-c"
DEFEITOS_C = AQUI / "defeitos-c"
PROJETOS = {"A": PROJETO, "B": PROJETO, "C": PROJETO_C}
DEFEITOS_DE = {"A": DEFEITOS, "B": DEFEITOS, "C": DEFEITOS_C}
REFERENCIA = AQUI / "referencia_test.py"
RODADAS = AQUI / "rodadas"
RESERVA = pathlib.Path.home() / ".local" / "bin"
TESTE = "test_carrinho.py"
FRASE_A = "Escreva os testes de unidade de carrinho.py em test_carrinho.py, com unittest."
FRASES = {
    "A": FRASE_A,
    "B": FRASE_A + " Antes de terminar, prove que os testes pegam defeito: plante um erro "
                   "no código, veja um teste falhar e desfaça.",
    "C": FRASE_A,
}
FERRAMENTAS = "Bash,Read,Write,Edit,Glob,Grep"
PERMITIDAS = "Bash(python *),Read,Write,Edit,Glob,Grep"


def hash_de(arquivo):
    return hashlib.sha256(pathlib.Path(arquivo).read_bytes()).hexdigest()


def defeitos(pasta=DEFEITOS):
    """Os mutantes, em ordem: d01_*.py a d10_*.py da pasta (defeitos/ ou defeitos-c/)."""
    return sorted(pathlib.Path(pasta).glob("d*.py"))


def sem_docstrings(arquivo):
    """ast.dump do arquivo sem as docstrings (módulo, classes e funções): o código só."""
    arvore = ast.parse(pathlib.Path(arquivo).read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        if isinstance(no, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            corpo = no.body
            if corpo and isinstance(corpo[0], ast.Expr) and isinstance(corpo[0].value, ast.Constant) \
                    and isinstance(corpo[0].value.value, str):
                no.body = corpo[1:]
    return ast.dump(arvore)


def comando(exe, condicao):
    """A linha de comando de uma rodada da condição."""
    global_md = (pathlib.Path.home() / ".claude" / "CLAUDE.md").as_posix()
    return [exe, "-p", FRASES[condicao], "--output-format", "json", "--no-session-persistence",
            "--setting-sources", "project,local",
            "--settings", json.dumps({"claudeMdExcludes": [global_md]}),
            "--tools", FERRAMENTAS, "--allowedTools", PERMITIDAS]


def uma_rodada(exe, condicao, n):
    with tempfile.TemporaryDirectory(prefix="tv", ignore_cleanup_errors=True) as tmp:
        pasta = pathlib.Path(tmp) / "loja"
        shutil.copytree(PROJETOS[condicao], pasta, ignore=shutil.ignore_patterns("__pycache__"))
        feito = subprocess.run(comando(exe, condicao), cwd=pasta, capture_output=True,
                               encoding="utf-8", errors="replace", check=False)
        gerado = pasta / TESTE
        teste = gerado.read_bytes() if gerado.is_file() else None
        codigo = pasta / "carrinho.py"
        alterado = not codigo.is_file() or hash_de(codigo) != hash_de(PROJETOS[condicao] / "carrinho.py")
        outros = sorted(p.relative_to(pasta).as_posix() for p in pasta.rglob("*")
                        if p.is_file() and "__pycache__" not in p.parts
                        and p.name not in ("carrinho.py", TESTE))
    if feito.returncode != 0:
        raise RuntimeError(f"claude saiu com {feito.returncode}: {feito.stderr.strip()[:300]}")
    dados = json.loads(feito.stdout)
    if dados.get("is_error"):
        raise RuntimeError(f"terminou em erro: {dados.get('subtype')}")
    destino = RODADAS / f"{condicao}-{n}"
    destino.mkdir(parents=True, exist_ok=True)
    if teste is not None:
        (destino / TESTE).write_bytes(teste)
    u = dados.get("usage", {})
    numeros = {
        "condicao": condicao,
        "n": n,
        "modelo": ",".join(sorted(dados.get("modelUsage", {}))),
        "turnos": dados.get("num_turns"),
        "duracao_s": round(dados.get("duration_ms", 0) / 1000, 1),
        "custo_usd": round(dados.get("total_cost_usd", 0), 4),
        "tokens_entrada": sum(u.get(k, 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                                     "cache_read_input_tokens")),
        "tokens_saida": u.get("output_tokens", 0),
        "teste_gerado": teste is not None,
        "carrinho_alterado": alterado,
        "outros_arquivos": outros,
        "quando": datetime.date.today().strftime("%d/%m/%Y"),
    }
    (destino / "numeros.json").write_text(json.dumps(numeros, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8")
    print(f"{condicao}-{n}: {numeros}", flush=True)


def rodar(rodadas, condicoes):
    exe = shutil.which("claude") or shutil.which("claude", path=os.fspath(RESERVA))
    if not exe:
        raise SystemExit("claude não encontrado no PATH nem em ~/.local/bin")
    falhas = []
    for n in range(1, rodadas + 1):
        for condicao in condicoes:
            if (RODADAS / f"{condicao}-{n}" / "numeros.json").exists():
                continue
            try:
                uma_rodada(exe, condicao, n)
            except (RuntimeError, json.JSONDecodeError) as erro:
                print(f"{condicao}-{n} FALHOU: {erro}", flush=True)
                falhas.append(f"{condicao}-{n}")
    if falhas:
        raise SystemExit(f"rodadas que falharam (rode de novo para refazer só elas): {falhas}")


def rodar_suite(teste, codigo):
    """Roda o arquivo de teste ao lado de uma cópia de codigo como carrinho.py.

    Devolve (código de saída do unittest, testes rodados, testes que falharam ou deram
    erro); o código é "tempo" se passar de 2 min."""
    teste = pathlib.Path(teste)
    with tempfile.TemporaryDirectory(prefix="tv", ignore_cleanup_errors=True) as tmp:
        tmp = pathlib.Path(tmp)
        shutil.copyfile(codigo, tmp / "carrinho.py")
        shutil.copyfile(teste, tmp / teste.name)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        try:
            feito = subprocess.run([sys.executable, "-m", "unittest", teste.stem], cwd=tmp,
                                   capture_output=True, encoding="utf-8", errors="replace",
                                   check=False, timeout=120, env=env)
        except subprocess.TimeoutExpired:
            return "tempo", 0, 0
    rodados = re.findall(r"^Ran (\d+) tests?", feito.stderr, re.M)
    falhas = re.findall(r"^FAILED \((.*)\)$", feito.stderr, re.M)
    caidos = sum(int(n) for n in re.findall(r"(?:failures|errors)=(\d+)", falhas[-1])) if falhas else 0
    return feito.returncode, int(rodados[-1]) if rodados else 0, caidos


def rodadas_gravadas():
    def chave(p):
        condicao, n = p.name.split("-")
        return condicao, int(n)
    if not RODADAS.is_dir():
        return []
    return sorted((p for p in RODADAS.iterdir() if (p / "numeros.json").is_file()), key=chave)


def faixa(valores):
    if not valores:
        return "-"
    return f"{min(valores)}–{max(valores)}, mediana {statistics.median(valores):g}"


def tabelas():
    """(medidas.tsv, defeitos.tsv) refeitos a partir das rodadas gravadas."""
    lista = defeitos()
    pastas = rodadas_gravadas()
    if not pastas:
        raise SystemExit("nenhuma rodada gravada: rode antes 'medir_teste_verde.py rodar'")
    medidas = ["condicao\tn\tmodelo\tturnos\tduracao_s\tcusto_usd\ttokens_entrada\ttokens_saida\t"
               "testes\tverde_no_certo\tdefeitos_pegos\tescaparam\tcarrinho_alterado"]
    detalhe = ["rodada\tdefeito\tresultado\ttestes_que_falharam"]
    resumo = {c: {"rodadas": 0, "verdes": 0, "pegos": [], "custo": 0.0, "tokens": []} for c in FRASES}
    escapes = {c: {d.stem: 0 for d in lista} for c in FRASES}
    margem = {c: {d.stem: [] for d in lista} for c in FRASES}
    for pasta in pastas:
        num = json.loads((pasta / "numeros.json").read_text(encoding="utf-8"))
        cond = num["condicao"]
        teste = pasta / TESTE
        certo = PROJETOS[cond] / "carrinho.py"
        rc, rodados, _ = rodar_suite(teste, certo) if teste.is_file() else ("sem_teste", 0, 0)
        verde = rc == 0 and rodados > 0
        escaparam = []
        for d in defeitos(DEFEITOS_DE[cond]):
            caidos = 0
            if not teste.is_file():
                resultado = "sem_teste"
            else:
                rc_d, _, caidos = rodar_suite(teste, d)
                pegou = rc_d != 0
                if verde:
                    resultado = "pegou" if pegou else "escapou"
                else:
                    resultado = ("falhou" if pegou else "passou") + "_nao_vale"
            if verde:
                margem[cond][d.stem].append(caidos)
            if resultado == "escapou":
                escaparam.append(d.stem.split("_")[0])
                escapes[cond][d.stem] += 1
            detalhe.append(f"{pasta.name}\t{d.stem}\t{resultado}\t{caidos}")
        pegos = len(lista) - len(escaparam) if verde else "nao_vale"
        r = resumo[num["condicao"]]
        r["rodadas"] += 1
        r["custo"] += num["custo_usd"]
        r["tokens"].append(num["tokens_entrada"] + num["tokens_saida"])
        if verde:
            r["verdes"] += 1
            r["pegos"].append(pegos)
        medidas.append("\t".join(str(v) for v in (
            num["condicao"], num["n"], num["modelo"], num["turnos"], num["duracao_s"],
            num["custo_usd"], num["tokens_entrada"], num["tokens_saida"], rodados,
            "sim" if verde else "nao", pegos, ",".join(escaparam) or "-",
            "sim" if num["carrinho_alterado"] else "nao")))
    rodape = [f"# {len(lista)} defeitos plantados; pegos contados só nas suítes verdes no certo"]
    for c, r in resumo.items():
        if r["rodadas"]:
            rodape.append(f"# {c}: {r['verdes']}/{r['rodadas']} suítes verdes no certo; defeitos pegos "
                          f"{faixa(r['pegos'])}; tokens {faixa(r['tokens'])}; "
                          f"custo total US$ {r['custo']:.2f}")
    for c, r in resumo.items():
        if r["rodadas"]:
            rodape.append(f"# {c}, escaparam (vezes, nas suítes verdes): " + (", ".join(
                f"{d} {v}" for d, v in sorted(escapes[c].items(), key=lambda kv: (-kv[1], kv[0])) if v)
                or "nenhum"))
            rodape.append(f"# {c}, testes que caíram com cada defeito, mínimo–máximo nas suítes "
                          "verdes: " + "; ".join(f"{d.split('_')[0]} {min(v)}–{max(v)}"
                                                 for d, v in margem[c].items() if v))
    return ("\n".join(medidas) + "\n\n" + "\n".join(rodape) + "\n",
            "\n".join(detalhe) + "\n")


def contar():
    medidas, detalhe = tabelas()
    (AQUI / "medidas.tsv").write_text(medidas, encoding="utf-8")
    (AQUI / "defeitos.tsv").write_text(detalhe, encoding="utf-8")
    print(medidas, end="")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["rodar"] and len(argv) <= 3:
        condicoes = [argv[2]] if len(argv) == 3 else list(FRASES)
        if any(c not in FRASES for c in condicoes):
            raise SystemExit(__doc__)
        rodar(int(argv[1]) if len(argv) >= 2 else 5, condicoes)
    elif argv == ["contar"]:
        contar()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
