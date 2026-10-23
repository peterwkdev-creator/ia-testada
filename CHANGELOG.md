# Histórico de versões

Cada versão tem uma tag `vX.Y.Z` no commit que a publicou. Medida nova ou
refeita entra aqui com a data e a pasta.

## A publicar

- Pasta nova `23-pr` (post 23): o `medir_pr.py`, que roda 5 vezes o
  `claude -p` pedindo a descrição do PR v0.4.0...v0.5.0 deste repositório
  (25 arquivos) e conta o que cada uma citou; as 5 descrições
  (`rodadas/`), a conferência à mão (`conferencia.tsv`, revisada por
  outro modelo), `arquivos.tsv` e `medidas.tsv` de 23/10/2026: 0 arquivo
  de fora, de 2 a 7 só pela pasta. `tests/test_23_pr.py`.
- Pasta nova `25-rebase` (post 25): o `medir_rebase.py`, sem IA, com
  remoto bare e dois clones; `medidas.tsv` de 23/10/2026 (git 2.56.0).
  `tests/test_25_rebase.py`.
- README: o 23 e o 25 no índice.

## 0.5.0 — 23/10/2026

- Pasta nova `31-agent-teams` (post 31): a tarefa (`TAREFA.md`), a
  configuração que liga o Agent Teams só no projeto do time
  (`settings-time.json`) e o `medir_time.py`, que chama o
  claude-context-cost nas duas pastas (cada uma copiada antes para um
  caminho curto, contra o `WinError 3` do 1.6.4) e grava o
  `medidas.tsv` de 23/10/2026: solo 141.260 tokens, time 564.642, 4,0×,
  e cada teammate pelo nome (cpf 127.088, temperatura 93.365, palavras
  125.961).
  `tests/test_31_agent_teams.py`.
- Pasta nova `30-motion` (post 30): o prompt testado em 21/10/2026 no
  claude.ai (`prompt.txt`), o HTML como saiu do chat (`widget.html`), a
  moldura de gravação (`index.html`), o gravador quadro a quadro
  (`gravar.py`, Playwright e ffmpeg) e os 18 números que a IA pôs na tela
  sem dado nenhum (`inventados.tsv`, com a linha de cada um).
  `tests/test_30_motion.py` confere o sha256 do HTML, a moldura, os 18
  valores e o prompt sem eles; os HTML entram como `binary` no
  `.gitattributes`, e o MP4 e os quadros ficam fora.
- Pasta nova `19-dicionario` (post 19): o trecho do gancho (`gancho.json`,
  3 eventos), a cópia da skill `programar-post` sem os ids da conta, os 22
  nomes do MCP Claude in Chrome e o `medir.py`, que refaz 3, 244, 4.921 e 22
  contra o `medidas.tsv`; `tests/test_19_dicionario.py`.
- README: o 30 no índice, no "Instalar" e no "Usar"; `requirements.txt` com
  o `playwright`.

## 0.4.0 — 21/10/2026

- `GUIA.md`: passo a passo para quem nunca rodou um medidor (clonar, Python
  3.11+, `python` ou `py` no Windows, os testes, um medidor, onde fica a
  transcrição, como ler a saída).
- README: índice de 01 a 07 em ordem, cada post com onde está o código
  (aqui, no `tts-ptbr` ou leitura de páginas oficiais, sem script) e "Antes
  de começar". Corrigido: não é "nada de `pip install`"; é a biblioteca
  padrão, menos o 07 (`claude-context-cost`) e o `capturar.py` do 05
  (`websockets` e Chrome), listados no `requirements.txt`.
- Pasta nova `02-releitura`: `medir_sessao.py`, cópia de 21/10/2026 do
  medidor que fez o post 2; o `--provar` dele virou
  `tests/test_02_releitura.py`, com transcrição sintética gerada no teste;
  `medicao-1810.txt` é a saída de 18/10/2026 (98,0% de releitura), com o id
  da transcrição trocado por `<sessão>`. Diferença do original: sem
  argumento, mostra o uso (como o 06 e o 07), em vez de procurar a
  transcrição pela pasta do projeto.
- Pasta nova `04-vozes`: README que aponta para o código e a medida do post
  4, em `tts-ptbr/exemplos/`.
- `05-agente`: `capturar.py` (as capturas do Reel, pelo Chrome sem tela) e
  `capturas/capturas.tsv` de 20/10/2026; testes só das partes puras (o CI
  não roda a captura). O `conferencia.tsv` mantém o nome.
- READMEs das pastas num modelo só: O que mede, Pré-requisitos, Passo a
  passo, Saída esperada, Como ler, Números, Fontes, Limites e correções.
  Nenhum número mudou.
- CI também em `windows-latest`; `.pytest_cache/` no `.gitignore`.

## 0.3.0 — 21/10/2026

- Pasta nova `07-subagente`: o `medir_subagentes.py` chama o
  claude-context-cost (`--json`) e grava só as contagens; `medidas.tsv` de
  21/10/2026 (passo do subagente 0,50 do da sessão: 48.272 contra 95.833
  tokens na mediana) e testes em `tests/`, inclusive do `main()`.

## 0.2.0 — 20/10/2026

- Pasta nova `05-agente`: o `conferir_fontes.py` confere se as frases que o
  post cita ainda estão nas páginas oficiais; `conferencia.tsv` de
  20/10/2026 (15 de 15 frases, 6 páginas, com os preços da API como fonte
  da "cobrança por uso") e testes em `tests/`, inclusive do `main()`.
- Erro de leitura que não é `OSError` (`http.client.IncompleteRead`) passa
  a sair no tsv como "erro:", em vez de traceback com o tsv antigo.
- `06-skill`: data prevista do post corrigida de 30/10 para 27/10/2026.

## 0.1.0 — 20/10/2026

- Primeira versão pública: a pasta `06-skill` (o que uma Skill custa no
  contexto do Claude Code), com o `medir_skills.py`, o `medidas.tsv` de
  20/10/2026 e os testes em `tests/`.
- Corrigido antes de publicar (20/10/2026): o `medir_skills.py` contava as
  aspas do YAML na descrição; a do `pptx` caiu de 962 para 960 caracteres e
  a do `xlsx`, de 952 para 950.
