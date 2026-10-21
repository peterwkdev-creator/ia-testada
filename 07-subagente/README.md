# 07-subagente: quanto custa o passo de um subagente

Medida do post sobre subagentes da @peterwk.dev (a publicar), no pilar
Corrigido: a gente achava que subagente custava ~110 mil tokens por passo,
e mediu metade disso.

**Medido em 21/10/2026, com o claude-context-cost v1.6.3**, no Windows,
nas transcrições de um projeto do Claude Code (o da própria @peterwk.dev).

## O que mede

Cada resposta do modelo relê o contexto inteiro da conversa; é esse
contexto, contado pelo uso da API gravado na transcrição, que se soma aqui.
Passo = uma resposta. O `medir_subagentes.py` compara:

1. o passo da sessão principal (mediana por sessão) contra o passo do
   subagente (mediana por subagente, com o menor e o maior);
2. quanto os subagentes pesam no projeto e em cada sessão que os chamou
   (o total dos subagentes da sessão sobre a sessão mais eles).

Não conta tokens por conta própria: chama o
[claude-context-cost](https://github.com/peterwkdev-creator/claude-context-cost)
com `--json`, que soma as sessões e os subagentes
(`<sessão>/subagents/*.jsonl`). A saída vai para o
[`medidas.tsv`](medidas.tsv) desta pasta, só com contagens: nenhum nome de
arquivo, id de sessão ou texto da conversa.

## Como refazer

```bash
pip install claude-context-cost
python -I medir_subagentes.py <pasta de um projeto em ~/.claude/projects>
```

No Windows a pasta é `%USERPROFILE%\.claude\projects\<pasta do projeto>`
(no macOS e no Linux, `~/.claude/projects/<pasta do projeto>`), uma por
projeto. Ela precisa ter subagentes: o script para com uma mensagem se não
tiver.

As transcrições são suas e têm dado da conta: não as publique nem as cole
em issue. O `.gitignore` deste repositório barra `*.jsonl`.

## Números (21/10/2026)

| Medida | Valor |
|---|---|
| passo da sessão principal (mediana de 44 sessões) | 95.833 tokens |
| passo do subagente (mediana de 34 subagentes) | 48.272 tokens |
| passo do subagente: menor e maior | 40.925 e 96.285 tokens |
| subagente ÷ sessão, por passo | 0,50 |
| subagentes no projeto | 17,8 mi de 282,2 mi tokens (6,3%) |
| peso dos subagentes na sessão que os chamou (17 sessões) | de 1,1% a 36,9% (mediana 9,5%) |

- O motivo provável, pela fonte 1: o subagente começa com contexto novo,
  sem a conversa da sessão. Não medimos a causa, só o custo por passo; o
  maior subagente (96.285) chega à mediana da sessão.
- A sessão desta medida estava aberta enquanto media: ela entra nos
  números com as respostas que tinha até ali, e o subagente que revisou
  este README é um dos 34.

## Fontes (lidas em 21/10/2026)

1. Claude Code, "Create custom subagents":
   https://code.claude.com/docs/en/sub-agents ("Each subagent starts with
   a fresh, isolated context window. It doesn't see your conversation
   history"; o *fork* é a exceção, "which inherits the parent conversation
   instead of starting fresh"; os pedidos do subagente "count toward the
   same usage limits as your main conversation").
2. claude-context-cost v1.6.3 (PyPI), o medidor que soma as transcrições:
   https://github.com/peterwkdev-creator/claude-context-cost

## Limites

- Um computador, um projeto, uma data, 34 subagentes. Um *fork* (que herda
  a conversa) começa com o contexto da sessão e não é o caso medido aqui.
- Tokens de contexto relido, não o preço: o cache barateia a releitura, e
  isso não entra aqui.
- Mediana por transcrição: uma sessão de 5 respostas pesa o mesmo que uma
  de 500 no passo da sessão.

## Correção de 21/10/2026

A conta que a gente usava (~110 mil tokens por passo de subagente) vinha
de 02/10/2026, quando 8 sessões e 23 subagentes juntos esgotaram o limite
de uso de 5 horas, e não de uma medida por passo. Medida aqui com o script,
por passo, deu 48 mil na mediana. Os passos daquele dia não foram medidos.
