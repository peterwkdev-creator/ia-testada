Aqui está a descrição. Não rodei os testes: o pedido para executá-los não foi aprovado. Por isso o plano de testes ficou como checklist a marcar.

---

**Título:** 0.5.0: pastas 19-dicionario, 30-motion e 31-agent-teams

## Resumo

Três pastas novas, cada uma com o material de um post (os três ainda não foram publicados). Também atualiza o índice do README e traz o CHANGELOG da 0.5.0, datada em 23/10/2026.

- **`19-dicionario` (post 19, pilar Dicionário):** hook, skill, MCP e subagente, e quem dispara cada um. Traz o trecho do gancho (`gancho.json`, 3 eventos), uma cópia da skill `programar-post` com os ids da conta Meta zerados e os 22 nomes de ferramenta do MCP Claude in Chrome. O `medir.py` refaz 3, 244, 4.921 e 22 e confere com o `medidas.tsv`; sai com 1 se algum valor não bater.
- **`30-motion` (post 30, pilar Testado):** o prompt de motion que viralizou, rodado em 21/10/2026 num chat anônimo do claude.ai. Inclui:
  - o `prompt.txt` exato;
  - o `widget.html` como saiu do chat, sem mudança;
  - a moldura de gravação `index.html` (1920x1080 e `window.tl = tl`);
  - o gravador quadro a quadro `gravar.py` (Playwright + ffmpeg);
  - os 18 números que a IA pôs na tela sem dado nenhum (`inventados.tsv`, com a linha de cada um).
- **`31-agent-teams` (post 31, pilar Medido):** a mesma tarefa feita por uma sessão só e por um líder com 3 teammates Sonnet. Deu **141.260 contra 564.642 tokens, 4,0×**, com todos os testes passando nos dois lados. Por teammate: cpf 127.088, temperatura 93.365, palavras 125.961.
  - O `medir_time.py` chama o claude-context-cost `--json` nas duas pastas. Antes, copia cada uma para um caminho curto, para evitar o `WinError 3` do 1.6.4.
  - O `settings-time.json` liga o Agent Teams só no projeto do time.

## Outras mudanças

- **README:**
  - o índice ganhou as linhas 19, 30 e 31;
  - uma nota explica que, do 7 em diante, o número é o do plano de posts (o 30 sai antes do 7);
  - o "Instalar" e o "Usar" foram atualizados (agora são cinco pastas com medidor).
- **`requirements.txt`:** `playwright` como dependência opcional, comentada, do `gravar.py`.
- **`.gitattributes`:** `30-motion/*.html` entra como `binary`, porque o teste confere o sha256 do HTML como saiu do chat.
- **`.gitignore`:** o MP4 e as pastas de quadros do 30 ficam fora, porque o `gravar.py` os refaz.
- **Correção para o CI do Linux:** o `longo()` do `medir_time.py` só põe o prefixo `\\?\` no Windows. Antes, fora do Windows, o `abspath` punha o diretório de trabalho na frente do caminho.

## Testes

Arquivos novos: `tests/test_19_dicionario.py`, `tests/test_30_motion.py` e `tests/test_31_agent_teams.py`. Todos usam só a biblioteca padrão.

- [ ] `python -m pytest` passa no CI (Linux e Windows)
- [ ] `python -I 19-dicionario/medir.py` dá `ok` nas 4 linhas
- [ ] `30-motion`: o sha256 do `widget.html` bate com o do teste depois do checkout (por causa do `binary` no `.gitattributes`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

Posso criar o PR com `gh pr create` usando esse texto, se você quiser.
