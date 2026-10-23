# 23-pr: o Claude Code escreve a descrição de um PR

Medida do post 23 da @peterwk.dev (a publicar), no pilar Medido: a mesma
frase, 5 vezes, pedindo ao Claude Code a descrição de um pull request real,
e a conferência, arquivo a arquivo, do que cada descrição citou. **Nenhum
dos 25 arquivos do diff ficou de fora em nenhuma rodada**; de 2 a 7 foram
citados só pela pasta.

**Medido em 23/10/2026, com o Claude Code 2.1.309 no modelo padrão (saiu
`claude-opus-5-5` nas 5 rodadas)**, no Windows.

## O que mede

O PR é deste repositório: a branch `pr-v0.5.0` (a tag `v0.5.0`) contra a
`main` em `v0.4.0`, 25 arquivos em 5 commits. Cada rodada monta um clone
novo numa pasta temporária, sem o remoto e sem as tags (a branch é a única
pista), e roda uma vez:

```
claude -p "Escreva a descrição do pull request desta branch para a main"
```

só com git, Read, Grep e Glob, sem guardar a sessão, sem os ganchos do
usuário e sem o `CLAUDE.md` global (`claudeMdExcludes`; o `--bare` não
serve com login de assinatura, só com chave de API).

Depois, cada arquivo do `git diff --name-status` vira uma de quatro
categorias: citado pelo **caminho**; pelo **nome** (o nome é único no diff,
ou a seção do texto deixa claro qual é); só pela **pasta**; ou **fora**. A
contagem automática marca como ambíguo o nome que se repete no diff
(`README.md`, `medidas.tsv`) e a conferência à mão decide.

## Pré-requisitos

- Python 3.11 ou mais novo.
- Git e o Claude Code com login (cada rodada custou de US$ 0,18 a 0,45).
- Este repositório clonado com as tags (`git fetch --tags`).

## Passo a passo

De dentro desta pasta (`cd 23-pr`):

```bash
python -I medir_pr.py rodar 5
python -I medir_pr.py contar
```

O `rodar` grava `rodadas/rodada-N.md` (a descrição) e `rodadas/rodada-N.json`
(modelo, turnos, duração, custo e tokens; nenhum texto da sessão). O
`contar` grava o [`medidas.tsv`](medidas.tsv) (uma linha por rodada) e o
[`arquivos.tsv`](arquivos.tsv) (rodada × arquivo, a categoria automática e
a final). As correções à mão ficam em [`conferencia.tsv`](conferencia.tsv),
com o motivo em cada linha; o `contar` as aplica.

## Números (23/10/2026)

| Rodada | Turnos | Tokens de entrada | US$ | Caminho | Nome | Pasta | Fora |
|---|---|---|---|---|---|---|---|
| 1 | 4 | 168.738 | 0,42 | 8 | 14 | 3 | 0 |
| 2 | 9 | 303.064 | 0,21 | 7 | 14 | 4 | 0 |
| 3 | 7 | 252.670 | 0,18 | 10 | 13 | 2 | 0 |
| 4 | 7 | 254.567 | 0,19 | 7 | 13 | 5 | 0 |
| 5 | 6 | 193.216 | 0,45 | 7 | 11 | 7 | 0 |

Três das 5 rodadas (1, 3 e 4) apontaram sozinhas que o
[`CHANGELOG.md`](../CHANGELOG.md) da 0.5.0 cita só o 30 no item do README,
mas o diff acrescenta ao índice também o 19 e o 31. A 2 e a 4 marcaram os
itens do "Como testar" que não conferiram.

## Limites

- 5 rodadas de um PR só, num repositório nosso e pequeno.
- A categoria "pasta" é conferida à mão: "cada README de pasta" não nomeia
  nenhum arquivo, e o critério está em cada linha do `conferencia.tsv`.
- O modelo padrão muda com a conta e com a versão do Claude Code.
