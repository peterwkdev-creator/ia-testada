# 06-skill: o que uma Skill custa no contexto

Medida do post "Skill: o que é um SKILL.md e o que não é" da @peterwk.dev
(a publicar; previsto para 30/10/2026).

**Medido em 20/10/2026, no Claude Code v2.1.299**, no Windows.

## O que mede

Uma Skill é uma pasta com um `SKILL.md`. No topo (YAML), nome e descrição:
a descrição entra na listagem de skills, no começo de toda conversa. O corpo
do `SKILL.md` só entra quando a skill é usada; os outros arquivos da pasta,
só quando lidos. O `medir_skills.py` põe número nisso:

1. cada `SKILL.md` em `~/.claude/skills`: caracteres da descrição, do
   `SKILL.md` inteiro e bytes dos outros arquivos da pasta da skill, e se ela
   entra na listagem (`disable-model-invocation: true` tira);
2. a listagem que entrou de fato no início da sessão: o anexo
   `skill_listing` da transcrição (quantas skills e quantos caracteres).

A saída vai para o [`medidas.tsv`](medidas.tsv) desta pasta, só com o nome
de cada skill e as contagens, nunca o caminho nem o conteúdo.

## Como refazer

```bash
python -I medir_skills.py <transcrição .jsonl de uma sessão do Claude Code>
```

A transcrição fica em `%USERPROFILE%\.claude\projects\<pasta do projeto>\<id da sessão>.jsonl`
no Windows (no macOS e no Linux, `~/.claude/projects/<pasta do projeto>/<id da sessão>.jsonl`),
uma pasta por projeto. A da sessão mais recente, no PowerShell:

```powershell
Get-ChildItem "$env:USERPROFILE\.claude\projects" -Recurse -Filter *.jsonl |
  Sort-Object LastWriteTime | Select-Object -Last 1 -ExpandProperty FullName
```

A transcrição é sua e tem dado da conta: não a publique nem a cole em issue.
O `.gitignore` deste repositório barra `*.jsonl`.

## Números (20/10/2026)

| Medida | Valor |
|---|---|
| skill `pptx`: SKILL.md | 28.424 caracteres |
| skill `pptx`: outros arquivos da pasta | 1.130.504 bytes (1,1 MB) |
| skill `pptx`: descrição | 960 caracteres |
| 17 skills da pasta: SKILL.md somados | 213.837 caracteres |
| 17 skills da pasta: outros arquivos | 3.872.841 bytes (3,9 MB) |
| descrições das 15 que entram na listagem | 9.776 caracteres |
| listagem inicial da sessão (19/10/2026, 19h59) | 36 skills, 18.738 caracteres |

- A pasta tinha 2 skills pessoais e 15 sincronizadas da conta do claude.ai
  pelo app desktop.
- A listagem tem 36 porque soma às da pasta as que vêm com o Claude Code e
  com os plugins; as 2 pessoais têm `disable-model-invocation: true` e não
  entram: só o usuário as chama.

## Fontes (lidas em 20/10/2026)

1. Claude Code, "Extend Claude with skills": https://code.claude.com/docs/en/skills
   (o corpo só carrega quando a skill é usada; cada skill da listagem soma
   ao contexto em toda resposta; a descrição é cortada em 1.536 caracteres
   na listagem).
2. Agent Skills, overview (Claude Platform):
   https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
   (três níveis: metadados sempre, corpo quando acionada, arquivos só quando
   lidos; `description` até 1.024 caracteres).

## Limites

- Um computador, uma sessão, uma data: a listagem muda com as skills e os
  plugins instalados e com a versão do Claude Code.
- Caracteres, não tokens: é o que se confere sem ferramenta. A doc fala em
  ~100 tokens por skill; não medimos tokens.
- A descrição é contada como está no YAML, numa linha; descrição em bloco
  (`|` ou `>`) não é tratada.

## Correção de 20/10/2026

A primeira versão do medidor contava as aspas do YAML como parte da
descrição: a do `pptx` dava 962 caracteres; sem as aspas, são 960 (a do
`xlsx`, de 952 para 950). O teste `tests/test_06_skill.py` fixa a regra.
