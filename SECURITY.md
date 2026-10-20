# Segurança

## Como avisar

Falha de segurança não vai em issue pública: use o aviso privado do GitHub,
em [Security → Report a vulnerability](https://github.com/peterwkdev-creator/ia-testada/security/advisories/new).
Diga a pasta da medida, o commit, o passo a passo para reproduzir e o efeito.

## O que esperar

- Primeira resposta em até 14 dias.
- A correção sai na última versão publicada; versões antigas não recebem
  correção.
- Crédito no [CHANGELOG.md](CHANGELOG.md) e no aviso, se você quiser.

## O que não é falha de segurança

Medida diferente da sua (um número, uma contagem, um caso que falta) é
issue comum, pelo modelo "Resultado diferente do medido".

O que os scripts fazem, para quem avalia o risco: o `06-skill/medir_skills.py`
lê os SKILL.md da sua pasta `~/.claude/skills` e a transcrição `.jsonl` que
você passar, e grava só o `medidas.tsv` da própria pasta, com o nome de cada
skill e contagens (nunca o caminho nem o conteúdo). Não pedem credencial, não
acessam a rede e não mandam nada para fora.
