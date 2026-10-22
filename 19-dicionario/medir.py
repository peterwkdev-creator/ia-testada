"""Refaz os números do post 19 que saem dos arquivos desta pasta.

Uso: python -I medir.py

Quatro medidas, conferidas contra o medidas.tsv (nesta pasta):
1. gancho_eventos: quantos eventos do gancho.json chamam o teto-passos.py.
2. skill_descricao_caracteres: o texto depois de "description: " no
   skill/SKILL.md (a parte que fica sempre no contexto).
3. skill_corpo_caracteres: o SKILL.md depois do topo YAML (a parte que só
   entra quando a skill é usada).
4. mcp_chrome_ferramentas: os nomes em mcp-chrome.txt.

O subagente (7 chamadas, 37.900 tokens, 30.739 ms) e a razão 0,50 não se
refazem daqui: vêm da notificação da tarefa e do 07-subagente.
Sai com 1 se alguma medida não bater com o medidas.tsv.
"""
import csv
import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent


def gancho_eventos(arquivo=AQUI / "gancho.json"):
    ganchos = json.loads(arquivo.read_text(encoding="utf-8"))["hooks"]
    return sum(1 for grupos in ganchos.values()
               if any("teto-passos.py" in h["command"]
                      for g in grupos for h in g["hooks"]))


def skill(arquivo=AQUI / "skill" / "SKILL.md"):
    """(caracteres da descrição, caracteres do corpo)."""
    texto = arquivo.read_text(encoding="utf-8")
    topo, corpo = texto.split("---", 2)[1:]
    descricao = re.search(r"^description: (.*)$", topo, re.M).group(1)
    return len(descricao), len(corpo)


def mcp_chrome(arquivo=AQUI / "mcp-chrome.txt"):
    return len(arquivo.read_text(encoding="utf-8").split())


def medir():
    descricao, corpo = skill()
    return {
        "gancho_eventos": gancho_eventos(),
        "skill_descricao_caracteres": descricao,
        "skill_corpo_caracteres": corpo,
        "mcp_chrome_ferramentas": mcp_chrome(),
    }


def gravadas(arquivo=AQUI / "medidas.tsv"):
    with open(arquivo, encoding="utf-8", newline="") as f:
        linhas = [l for l in f if l.strip() and not l.startswith("#")]
    return {l["medida"]: l["valor"] for l in csv.DictReader(linhas, delimiter="\t")}


def main():
    esperado = gravadas()
    erros = 0
    for medida, valor in medir().items():
        ok = str(valor) == esperado.get(medida)
        erros += not ok
        print(f"{medida:28} {valor:>6}  {'ok' if ok else 'medidas.tsv diz ' + str(esperado.get(medida))}")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
