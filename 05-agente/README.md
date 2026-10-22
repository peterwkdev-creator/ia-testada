# 05-agente: "publique seu agente em 5 minutos" no claude.ai

Prova do post "'Publique seu agente em 5 minutos': no claude.ai, isso não
existe" da @peterwk.dev (a publicar; previsto para 30/10/2026). A pasta é a
05; na ordem de publicação, é o post 6 (as datas do 05 e do 06 trocaram em
20/10/2026, e as pastas não mudam de nome).

**Conferido em 20/10/2026**, nas páginas oficiais abaixo.

## O que mede

O post não mede um número: ele cita páginas oficiais. Página de documentação
muda sem aviso (a do Managed Agents ganhou "scheduled deployments" entre 18 e
20/10/2026). Dois scripts:

1. `conferir_fontes.py` baixa cada página e confere, frase a frase, se o
   trecho citado no post ainda está lá. A saída vai para o
   [`conferencia.tsv`](conferencia.tsv), com a data e a hora da leitura
   (UTC), e o script sai com código 1 se alguma frase sumiu.
2. `capturar.py` faz as capturas de tela do Reel: abre duas páginas da
   Central de Ajuda num Chrome sem tela, marca a frase citada com um
   retângulo verde e recorta uma faixa de 1080 px. Grava
   `capturas/<nome>.png` e o [`capturas/capturas.tsv`](capturas/capturas.tsv)
   (nome, URL, frase, resultado, data UTC).

O arquivo se chama `conferencia.tsv` (e não `medidas.tsv`, como no 06 e no
07) porque aqui não há medida: há a conferência de frases.

## Pré-requisitos

- Python 3.11 ou mais novo e rede.
- `conferir_fontes.py`: só a biblioteca padrão.
- `capturar.py`: `pip install websockets` e o Google Chrome. No Windows o
  script procura o Chrome em `C:\Program Files\Google\Chrome\Application\chrome.exe`;
  noutro lugar (ou no macOS e no Linux), diga onde pela variável de
  ambiente `CHROME`: o caminho completo do executável do Chrome. Sem ela, o
  script usa o caminho do Windows acima.

Nenhum dos dois lê a sua conta. O `capturar.py` usa um perfil do Chrome
próprio e vazio, na pasta temporária do sistema: não usa o seu perfil, os
seus logins nem os seus cookies.

## Passo a passo

1. Entre na pasta: `cd 05-agente`.
2. Confira as frases:

   ```bash
   python -I conferir_fontes.py
   ```

3. Se quiser refazer as capturas (opcional):

   ```bash
   pip install websockets
   python capturar.py
   ```

   Com o Chrome noutro lugar, defina `CHROME` antes. No Windows
   (PowerShell), por exemplo:

   ```powershell
   $env:CHROME = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
   python capturar.py
   ```

   No macOS (no Linux, algo como `/usr/bin/google-chrome`):

   ```bash
   export CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   python capturar.py
   ```

## Saída esperada

- `conferir_fontes.py`: uma linha por frase, com `sim` ou `não` na frente,
  e no fim `lido em <data> UTC; N de M frases ...`. Código de saída 0 se
  todas estão lá; 1 se alguma sumiu.
- `capturar.py`: `projeto: ok (...)` e `artefato: ok (...)`, os dois PNG em
  `capturas/` e o `capturas.tsv` reescrito. Código 1 se alguma frase não foi
  achada.

## Como ler

A afirmação do post: no claude.ai não há como publicar um agente como app
ou bot para o público:

- o Projeto do chat só se compartilha dentro da organização, nos planos Team
  e Enterprise;
- o que se compartilha é o artefato, e quem o usa gasta o próprio plano;
- um agente que roda para outras pessoas existe, mas pela API (Agent SDK ou
  Managed Agents), com chave de API e cobrança por uso.

Vale para o claude.ai e para as páginas lidas na data da conferência. Não
dizemos que "não existe agente publicável": pela API, existe. Uma frase com
`não` quer dizer que a página mudou: o post precisa ser revisto.

## Números (20/10/2026)

| Medida | Valor |
|---|---|
| frases citadas presentes nas páginas (`conferencia.tsv`, 23:14 UTC) | 15 de 15, em 6 páginas |
| capturas com a frase achada (`capturas/capturas.tsv`, 23:23 UTC) | 2 de 2 |

## Fontes (lidas em 20/10/2026)

1. Compartilhar Projeto (Central de Ajuda):
   https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing
2. Artefatos (Central de Ajuda):
   https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them
3. Agent SDK, overview: https://code.claude.com/docs/en/agent-sdk/overview
4. Managed Agents, overview (beta): https://platform.claude.com/docs/en/managed-agents/overview
5. Projects do Claude Code (para não confundir com os do chat):
   https://code.claude.com/docs/en/claude-projects
6. Preços da API (a "cobrança por uso": tokens e, no Managed Agents, tempo
   de sessão): https://platform.claude.com/docs/en/about-claude/pricing

## Limites e correções

- A frase estar na página não diz que nada mudou em volta dela: o script
  confere o trecho citado, não a página inteira.
- A afirmação central é uma ausência ("não há opção de publicar"), e frase
  presente não prova ausência: se um botão de publicar surgir, o script não
  vê. Essa parte vale pela leitura das páginas na data acima.
- A Central de Ajuda não traz data de atualização ("Updated over a week
  ago"): o que vale é a data da leitura.
- Os planos Team e Enterprise não foram conferidos por dentro; o que se diz
  deles vem da página 1.
- O CI não roda o `capturar.py` (precisa de rede e de Chrome): os testes
  (`tests/test_05_capturar.py`) cobrem só o recorte, o tsv e o
  `capturas.tsv` guardado. As imagens não vão para o repositório; o script
  as refaz.
- O `capturar.py` publicado aqui é de 21/10/2026; as capturas de
  20/10/2026 saíram de uma versão anterior. Mudou só o que não altera a
  captura (o `websockets` carregado na hora, a
  variável `CHROME` e o recorte e o tsv em funções testáveis).
