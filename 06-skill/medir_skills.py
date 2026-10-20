"""Mede o que uma Skill custa no contexto: a descrição contra o resto.

Uso: python -I medir_skills.py <transcrição .jsonl de uma sessão do Claude Code>

Duas medidas, gravadas em medidas.tsv (nesta pasta):
1. Cada SKILL.md em ~/.claude/skills (pessoais e as sincronizadas do
   claude.ai): caracteres da descrição, do SKILL.md inteiro e bytes dos
   outros arquivos da pasta da skill. Só o nome da skill entra na saída,
   nunca o caminho (a pasta "synced" tem ids da conta).
2. A listagem de skills que entrou de fato no início da sessão: o anexo
   "skill_listing" da transcrição (quantas skills e quantos caracteres).
"""
import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
SKILLS = pathlib.Path.home() / ".claude" / "skills"


def descricao(topo):
    """Caracteres da descrição no topo YAML do SKILL.md; 0 se não houver."""
    desc = re.search(r"^description:\s*(.*)$", topo, re.M)
    if not desc:
        return 0
    # sem as aspas do YAML, que não fazem parte do texto (20/10: o pptx dava 962, são 960)
    return len(re.sub(r'^(["\'])(.*)\1$', r"\2", desc.group(1).strip()))


def skills(pasta=SKILLS):
    for p in sorted(pathlib.Path(pasta).rglob("SKILL.md"), key=lambda p: p.parent.name):
        t = p.read_text(encoding="utf-8")
        fim = t.index("\n---", 4)
        topo = t[:fim]
        so_usuario = re.search(r"^disable-model-invocation:\s*true", topo, re.M)
        outros = sum(f.stat().st_size for f in p.parent.rglob("*")
                     if f.is_file() and f.name != "SKILL.md")
        yield (p.parent.name, descricao(topo), len(t), outros,
               "não" if so_usuario else "sim")


def listagem(jsonl):
    with open(jsonl, encoding="utf-8") as fh:
        for linha in fh:
            r = json.loads(linha)
            a = r.get("attachment")
            if r.get("type") == "attachment" and isinstance(a, dict) \
                    and a.get("type") == "skill_listing" and a.get("isInitial"):
                return a["skillCount"], len(a["content"]), r.get("timestamp", "")
    raise SystemExit("sem skill_listing inicial nesta transcrição")


def tabela(linhas, n, chars, quando):
    saida = ["skill\tdescricao_chars\tskill_md_chars\toutros_bytes\tna_listagem"]
    saida += ["\t".join(map(str, l)) for l in linhas]
    saida += ["", f"# listagem inicial da sessão ({quando}): {n} skills, {chars} caracteres"]
    return "\n".join(saida) + "\n"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    linhas = list(skills())
    texto = tabela(linhas, *listagem(sys.argv[1]))
    (AQUI / "medidas.tsv").write_text(texto, encoding="utf-8")
    print(texto, end="")


if __name__ == "__main__":
    main()
