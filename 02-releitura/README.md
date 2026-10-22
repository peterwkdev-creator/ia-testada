# 02-releitura: onde vão os tokens de uma sessão

Medida do post "Claude Code: medi onde vão os tokens de uma sessão de IA, e
96% são o Claude relendo a conversa" da @peterwk.dev (post 2, publicado em
19/10/2026).

**Medido em 29/09/2026 e de novo em 18/10/2026.** A sessão medida de
18/10/2026 rodou no Claude Code v2.1.299, plano Max, no Windows.

## O que mede

A cada resposta, a conversa inteira entra de novo pelo cache. O
`medir_sessao.py` lê a transcrição de uma sessão (um JSON por linha) e soma
o `usage` de cada resposta em quatro partes:

1. releitura do cache (`cache_read_input_tokens`);
2. gravação do cache (`cache_creation_input_tokens`);
3. entrada nova (`input_tokens`);
4. saída, o texto que o Claude escreveu (`output_tokens`).

Uma resposta grava um bloco por linha. O `usage` se repete em todas essas
linhas. Por isso o script conta uma vez por `message.id`.

Ele mostra também três coisas:

- o contexto por resposta (mediana, p90 e máximo);
- os reinícios de cache, quando mais de 100 mil tokens são gravados de uma
  vez;
- quanto texto cada ferramenta devolveu.

## Pré-requisitos

- Python 3.11 ou mais novo, só a biblioteca padrão.
- O Claude Code instalado, com pelo menos uma sessão feita.

## Passo a passo

1. Ache a transcrição. No Windows:
   `%USERPROFILE%\.claude\projects\<pasta do projeto>\<id da sessão>.jsonl`
   (no macOS e no Linux, `~/.claude/projects/<pasta do projeto>/<id da sessão>.jsonl`).
   O [GUIA](../GUIA.md) mostra como achar a mais recente.
2. Entre na pasta (`cd 02-releitura`) e rode:

   ```bash
   python -I medir_sessao.py <transcrição .jsonl de uma sessão do Claude Code>
   ```

   Sem argumento (ou com mais de um), ele mostra como usar e sai sem medir
   nada.

### O teste que roda numa transcrição sua

Um dos testes (`tests/test_02_releitura.py`) fica `skipped` no
`python -m unittest`: ele só roda se a variável de ambiente
`IA_TESTADA_TRANSCRICAO` tiver o caminho de uma transcrição `.jsonl` sua.
Ele confere se as somas do script batem com uma conta independente nela.
Na raiz do repositório:

- Windows (PowerShell):

  ```powershell
  $env:IA_TESTADA_TRANSCRICAO = "$env:USERPROFILE\.claude\projects\<pasta do projeto>\<id da sessão>.jsonl"
  python -m unittest tests.test_02_releitura -v
  ```

- macOS e Linux:

  ```bash
  IA_TESTADA_TRANSCRICAO=~/.claude/projects/<pasta do projeto>/<id da sessão>.jsonl python -m unittest tests.test_02_releitura -v
  ```

A transcrição é sua e tem dado da conta: não a publique nem a cole em issue.
O `.gitignore` deste repositório barra `*.jsonl`. O script só lê; a saída
vai para a tela.

## Saída esperada

O formato da [`medicao-1810.txt`](medicao-1810.txt), a saída de 18/10/2026
(com o id da transcrição trocado por `<sessão>`):

```text
transcript: <sessão>.jsonl  (3.1 MB)
respostas: 127
  cache_read_input_tokens            13,257,338   98.0%
  cache_creation_input_tokens           210,640    1.6%
  output_tokens                          61,085    0.5%
  input_tokens                              260    0.0%
contexto por resposta: mediana 101,801 · p90 153,172 · máx 165,865
```

Seguem os reinícios de cache e as 8 ferramentas que mais devolveram texto.

## Como ler

- A porcentagem de `cache_read_input_tokens` é a releitura: quanto do
  volume foi a conversa entrando de novo. Ler do cache é barato por token,
  mas é quase todo o volume.
- `output_tokens` é o texto que o Claude escreveu: a menor parte.
- O gasto é o tamanho do contexto vezes o número de passos: a mediana do
  contexto por resposta diz quanto cada passo relê.

## Números

| Medida | 29/09/2026 (sessão de 7 dias) | 18/10/2026 |
|---|---|---|
| respostas | 553 | 127 |
| releitura do cache | 235 mi (96%) | 13,3 mi (98,0%) |
| gravação do cache | 9,5 mi | 0,2 mi (1,6%) |
| saída | 0,6 mi (0,2%) | 61.085 (0,5%) |

A de 29/09 é a contagem corrigida em 01/10/2026; a de 18/10 é a sessão de
18/10/2026.

## Fontes

1. Prompt caching (Claude Platform), o que é ler e gravar no cache:
   https://platform.claude.com/docs/en/build-with-claude/prompt-caching
   (lida em 18/10/2026).
2. Medição própria: `medir_sessao.py`, 29/09 e 18/10/2026.

## Limites e correções

- Uma sessão, um computador, uma data: a sua pode dar diferente.
- Tokens, não preço: ler do cache custa menos por token que gravar ou
  escrever, e isso não entra aqui.
- **A medida de 29/09 não tem saída guardada.** A transcrição daquele dia
  não existe mais; os números vêm do registro da medição (contagem
  corrigida em 01/10/2026). Só a de 18/10 está aqui, em `medicao-1810.txt`.
- **Correção de 01/10/2026.** A primeira contagem de 29/09 dava 0,3% de
  saída; corrigida, 0,2%.
- **Por que uma cópia.** O `medir_sessao.py` é a cópia, feita em
  21/10/2026, do medidor de uso interno que fez o post. A conta é a mesma.
  Em 21/10/2026 testamos o
  [claude-context-cost](https://github.com/peterwkdev-creator/claude-context-cost)
  1.6.4 para isso: ele dá o total de entrada por fonte (CLAUDE.md, regras,
  skills), mas não separa releitura, gravação e saída. O `--provar` do
  original virou `tests/test_02_releitura.py`, com transcrição sintética
  gerada no teste.
