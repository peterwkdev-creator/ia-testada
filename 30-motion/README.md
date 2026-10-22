# 30-motion: o prompt de motion que viralizou, testado

Teste do post 30 da @peterwk.dev (a publicar), no pilar Testado. Um post
que circulou prometia "motion graphics de nível profissional usando só o
Claude". Rodamos o prompt 1 dele, preenchido com a nossa marca, e
gravamos o resultado em MP4.

**Testado em 21/10/2026, no claude.ai:** chat anônimo (sem histórico nem
memória), Opus 5.5 com raciocínio Alto, uma tentativa. Gravado em MP4 no
Windows, com Playwright e ffmpeg.

## O que mede

1. Se o prompt sai de primeira: o HTML que o chat entregou, sem mudança, em
   [`widget.html`](widget.html).
2. Quais números a IA pôs na tela sem que nenhum estivesse no prompt: os 18
   valores de [`inventados.tsv`](inventados.tsv), com a linha de cada um no
   `widget.html`.
3. O passo do HTML ao vídeo, que o post não mostra: o
   [`gravar.py`](gravar.py) grava a animação quadro a quadro.

Arquivos:

- [`prompt.txt`](prompt.txt): o texto exato enviado, num parágrafo só.
- [`widget.html`](widget.html): o HTML como saiu do chat (28.708 bytes, 289
  linhas, a última sem quebra de linha: o `wc -l` conta 288).
- [`index.html`](index.html): a moldura de gravação. É o `widget.html`
  inteiro, sem mudança, com o tamanho fixo em 1920x1080, os controles do
  player escondidos e uma linha a mais, `window.tl = tl`, para o gravador
  achar a timeline.
- [`gravar.py`](gravar.py): o gravador. Difere do que gravou o Reel em
  22/10/2026 só em duas coisas, pedidas na revisão: o servidor local não
  escreve cada pedido na tela, e o Chrome e o servidor fecham mesmo quando
  a gravação falha no meio.
- [`inventados.tsv`](inventados.tsv): os números da tela que não vieram de
  dado nenhum.

## Pré-requisitos

- Python 3.11 ou mais novo.
- `python -m pip install playwright` (o gravador usa o Google Chrome
  instalado; não precisa de `playwright install`).
- O [ffmpeg](https://ffmpeg.org/) no PATH, ou o caminho dele em `--ffmpeg`.
  Para conferir se está instalado: `ffmpeg -version`. No Windows, instala
  com `winget install ffmpeg` (feche e abra o terminal depois).
- Internet: o `widget.html` carrega o GSAP e as fontes pela rede, como saiu
  do chat. Sem rede, a gravação para no começo, com erro de tempo esgotado
  (o gravador espera até 10 s pela animação).

## Passo a passo

Para ver a animação, abra o `widget.html` no navegador. Para gravar, de
dentro desta pasta (`cd 30-motion`):

```bash
python -m pip install playwright
python gravar.py index.html teste.mp4 --seg 30
```

Para refazer o teste no claude.ai: chat anônimo, cole o `prompt.txt`, uma
tentativa. Sai outro HTML, com outros números: compare com o
`inventados.tsv`.

## Saída esperada

`teste.mp4` (1920x1080, 30 fps, 900 quadros, 30,000 s) e a pasta
`teste-quadros/` com os PNGs. Na tela, a cada 5 s, o quadro, o tempo
esperado e o da timeline, que têm de bater:

```
quadro    0  esperado   0.00 s  tl   0.00 s
quadro  150  esperado   5.00 s  tl   5.00 s
...
900 quadros -> .../teste.mp4
```

Gravado em 22/10/2026: 56,4 s no relógio, do início ao fim da gravação.

## Como ler

- O relógio do navegador é falso, de propósito: cada quadro avança 1/30 s
  exato. O vídeo não depende da velocidade da máquina, e o tempo da
  timeline confirma.
- O `inventados.tsv` dá, para cada valor, as linhas do `widget.html` onde o
  conferimos, e o teste confere que o valor está nelas. A lista de linhas
  não é exaustiva: um valor curto pode aparecer em outras.
- "Inventado" quer dizer que o valor não veio de dado nenhum que demos. Não
  dizemos que a IA "mente". A frase "Cada número com fonte e data" era
  nossa, uma das cenas do prompt; os valores, a fonte e a data, não.

## Números (21 e 22/10/2026)

| Medida | Valor |
|---|---|
| tempo de raciocínio (lido na página do chat) | 6 min 44 s |
| resposta pronta | ~8 min (507 s) |
| roda de primeira | sim: uma resposta, nenhuma correção |
| números inventados na tela | 18 valores distintos, 26 ocorrências como fato |
| números no prompt | 2: "1920x1080" e "30s" |
| 71,3% inteiro na tela | do quadro 262 ao 333 (8,73 a 11,13 s) |
| gravação | 900 quadros, 30,000 s, `tl` igual ao esperado nos 6 pontos |

- O mais forte: "71,3%" com "fonte · relatório oficial" e "data · 14 out
  2026", e "1,84 s" com "fonte · teste próprio" e "data · 15 out 2026".
  Não há relatório nem teste.
- O "10x" aparece riscado como alegação de um "post viral" e, adiante, como
  "afirma: 10x mais rápido" contra um "1,3x" de "resultado real", também
  sem medida. Não entra nos 18: a própria tela o trata como falso.
- A própria resposta avisou que aquilo "só se sustenta se os números vierem
  do mesmo teste real".
- Incoerência interna: "3/50" erros não bate com 71,3% de precisão.

## Fontes

1. O prompt 1 de um carrossel do Instagram de 05/10/2026 ("5 prompts" de
   motion com o Claude), preenchido com a nossa marca. O post não é citado
   aqui pelo nome: o teste é do formato, não da pessoa.
2. GSAP (a biblioteca de animação que o HTML usa): https://gsap.com/
3. Playwright para Python, `add_init_script` (o que troca o relógio antes
   da página): https://playwright.dev/python/docs/api/class-page

## Limites e correções

- Um prompt (o 1 de 5), uma tentativa, uma data, uma conta. Não testamos os
  outros 4 prompts nem outros modelos. Rodado de novo, o mesmo prompt dá
  outro HTML.
- O chat não deixa ver o HTML como arquivo: sai num visualizador com
  player. Copiamos o código pela área de transferência; o tamanho e o
  número de linhas batem com o do chat.
- **Correção de 22/10/2026.** A primeira versão do gravador não era
  determinística: a cena 7 sorteia a ordem dos elementos
  (`stagger from:'random'`), e duas gravações diferiam nos quadros 724 a 757
  (24,13 a 25,23 s). O `gravar.py` daqui fixa a semente do `Math.random`;
  o HTML da IA fica igual.
- Um teste anterior, por um subagente do Claude Code, não entra aqui: ele
  recebe o contexto do projeto e puxou números do nosso próprio git.
