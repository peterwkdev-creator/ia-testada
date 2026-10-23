Aqui está a descrição, montada a partir dos 5 commits da `pr-v0.5.0` e do diff contra a `main`:

---

**Título:** 0.5.0: pastas 19-dicionario, 30-motion e 31-agent-teams

## O que entra

Três pastas novas, cada uma com o código e os números de um post, e um teste para cada.

### `31-agent-teams` (post 31, medido em 23/10/2026)
Pusemos a mesma tarefa para uma sessão só e para um líder com 3 teammates.
- `TAREFA.md`: a tarefa.
- `settings-time.json`: liga o Agent Teams só no projeto do time.
- `medir_time.py`: chama o claude-context-cost nas duas pastas. Antes, copia cada uma para um caminho curto, contra o `WinError 3` do 1.6.4. Fora do Windows, `longo()` devolve o caminho como veio, o que corrige o CI do Linux.
- `medidas.tsv`: solo **141.260** tokens, time **564.642**, **4,0×**. Por teammate: cpf 127.088, temperatura 93.365, palavras 125.961.
- `tests/test_31_agent_teams.py`.

### `30-motion` (post 30, testado em 21/10/2026)
- `prompt.txt`: o prompt testado no claude.ai.
- `widget.html`: o HTML como saiu do chat.
- `index.html`: a moldura de gravação.
- `gravar.py`: o gravador quadro a quadro (Playwright e ffmpeg).
- `inventados.tsv`: os **18 números** que a IA pôs na tela sem ter dado nenhum, com a linha de cada um.
- `tests/test_30_motion.py`: confere o sha256 do HTML, a moldura, os 18 valores e que o prompt não contém nenhum deles.
- `.gitattributes`: `30-motion/*.html` entra como `binary`, para o sha256 não mudar com conversão de fim de linha.
- `.gitignore`: o MP4 e as pastas de quadros ficam fora; o `gravar.py` os refaz.

### `19-dicionario` (post 19, medido em 22/10/2026)
- `gancho.json`: o trecho do gancho, com 3 eventos.
- `skill/SKILL.md`: cópia da skill `programar-post`, sem os ids da conta.
- `mcp-chrome.txt`: os 22 nomes de ferramentas do MCP Claude in Chrome.
- `medir.py`: refaz 3, 244, 4.921 e 22 e compara com o `medidas.tsv`.
- `tests/test_19_dicionario.py`.

### Raiz
- `README.md`:
  - Os posts 19, 30 e 31 entram na tabela.
  - O "Instalar" passa a citar o claude-context-cost do 31 e o `playwright`, o Chrome e o ffmpeg do 30.
  - O "Usar" vai para cinco pastas com medidor.
  - Uma nota explica que, do 7 em diante, o número da pasta é o do plano de posts, e que a data de publicação pode furar a fila: o 30 sai antes do 7.
- `requirements.txt`: `playwright` comentado, como as outras dependências opcionais.
- `CHANGELOG.md`: entrada 0.5.0, datada em 23/10/2026.

## Como conferir

```bash
python -m unittest discover tests
```

Os testes só usam a biblioteca padrão; nenhum precisa do Playwright, do ffmpeg ou do claude-context-cost. Para refazer as medidas, cada README de pasta tem o passo a passo.

## Depois do merge
Criar a tag `v0.5.0` no commit do merge.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

O último item do 0.5.0 no `CHANGELOG.md` diz "README: o 30 no índice, no 'Instalar' e no 'Usar'". Só que o README também ganhou o 19 e o 31 na tabela, o 19 e o 31 no "Usar" e o 31 no "Instalar". Se quiser, ajusto essa linha antes de abrir o PR. Também posso abrir o PR com `gh pr create` usando este texto.
