Segue a descrição, no template do repositório (`.github/pull_request_template.md`):

---

**Título:** 0.5.0: pastas 19-dicionario, 30-motion e 31-agent-teams

**O que muda**

Três pastas novas, cada uma com o código e as medidas de um post, mais os testes delas. Também atualiza o README da raiz (índice, "Instalar", "Usar") e o CHANGELOG, com a 0.5.0 datada em 23/10/2026.

- **`31-agent-teams` (post 31):** a mesma tarefa (`TAREFA.md`) feita por uma sessão só e por um líder com 3 teammates. O `settings-time.json` liga o Agent Teams só no projeto do time. O `medir_time.py` chama o claude-context-cost nas duas pastas: copia cada uma antes para um caminho curto, contra o `WinError 3` do 1.6.4, e grava o `medidas.tsv` de 23/10/2026: solo 141.260 tokens, time 564.642 (4,0×), e cada teammate pelo nome (cpf 127.088, temperatura 93.365, palavras 125.961). Fora do Windows, `longo()` devolve o caminho como veio, o que corrige o CI do Linux. Teste: `tests/test_31_agent_teams.py`.
- **`30-motion` (post 30):** o prompt testado em 21/10/2026 no claude.ai (`prompt.txt`), o HTML como saiu do chat (`widget.html`), a moldura de gravação (`index.html`) e o gravador quadro a quadro (`gravar.py`, com Playwright e ffmpeg). O `inventados.tsv` traz os 18 números que a IA pôs na tela sem dado nenhum, com a linha de cada um. `tests/test_30_motion.py` confere:
  - o sha256 do HTML;
  - a moldura;
  - os 18 valores;
  - que o prompt não traz nenhum deles.

  Os HTML entram como `binary` no `.gitattributes`, e o MP4 e os quadros ficam no `.gitignore`.
- **`19-dicionario` (post 19):** o trecho do gancho (`gancho.json`, 3 eventos), uma cópia da skill `programar-post` sem os ids da conta e os 22 nomes do MCP Claude in Chrome (`mcp-chrome.txt`). O `medir.py` refaz os números 3, 244, 4.921 e 22 e compara com o `medidas.tsv`. Teste: `tests/test_19_dicionario.py`.
- **Raiz:** linhas 19, 30 e 31 no índice, com uma nota de que, do post 7 em diante, o número segue o plano de posts e a data pode furar a fila. `requirements.txt` ganha o `playwright`, comentado como as outras dependências opcionais.

**Conferência**

- [ ] `python -m unittest` passa.
- [x] Medidor novo ou alterado tem teste com dados inventados e o resultado esperado escrito à mão.
- [x] Medida nova ou refeita traz data, versão do que foi medido, fonte com URL, como refazer e limites no README da pasta.
- [x] Nada de dado privado: transcrição, caminho com id da conta, e-mail ou token.
- [x] Texto em português; mudança de medida ou de comportamento no CHANGELOG.md.
- [x] Código próprio, sob a licença MIT do projeto (ver CONTRIBUTING.md).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

O `python -m unittest` precisava de aprovação e não rodou, então deixei esse item desmarcado; marque depois de rodar, ou quando o CI passar. Os outros itens marquei a partir do diff e do CHANGELOG, sem abrir cada README de pasta, então vale conferir antes de publicar. Se quiser, eu abro o PR com `gh pr create`.
