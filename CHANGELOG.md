# Histórico de versões

Cada versão tem uma tag `vX.Y.Z` no commit que a publicou. Medida nova ou
refeita entra aqui com a data e a pasta.

## 0.4.0 (a publicar)

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
