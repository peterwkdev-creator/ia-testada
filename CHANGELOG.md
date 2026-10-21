# Histórico de versões

Cada versão tem uma tag `vX.Y.Z` no commit que a publicou. Medida nova ou
refeita entra aqui com a data e a pasta.

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
