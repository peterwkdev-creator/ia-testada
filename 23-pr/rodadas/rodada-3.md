A execução dos testes precisava de aprovação e não rodou, então deixei esse item sem marcar no "Como testar". A descrição saiu dos cinco commits da branch e do diff contra a `main`:

---

**Título:** v0.5.0: pastas 19-dicionario, 30-motion e 31-agent-teams

## Resumo

Esta branch traz o material de três posts, cada um em uma pasta nova com teste, e fecha a versão 0.5.0 (CHANGELOG datado em 23/10/2026).

### `31-agent-teams` (post 31)
- `TAREFA.md`: a tarefa feita duas vezes, por uma sessão só e por um líder com 3 teammates.
- `settings-time.json`: liga o Agent Teams só no projeto do time.
- `medir_time.py`: chama o `claude-context-cost` nas duas pastas e grava o `medidas.tsv`. Antes, copia cada pasta para um caminho curto, para evitar o `WinError 3` da versão 1.6.4.
- Resultado de 23/10/2026: **solo 141.260 tokens, time 564.642 (4,0×)**. Por teammate: cpf 127.088, temperatura 93.365, palavras 125.961.
- `tests/test_31_agent_teams.py`.
- Correção no CI do Linux: fora do Windows, `longo()` devolve o caminho como veio. Antes, o `abspath` punha o diretório de trabalho na frente do prefixo `\\?\`; agora o prefixo só entra no Windows.

### `30-motion` (post 30)
- `prompt.txt`: o prompt testado no claude.ai em 21/10/2026.
- `widget.html`: o HTML como saiu do chat.
- `index.html`: a moldura de gravação.
- `gravar.py`: gravador quadro a quadro, com Playwright e ffmpeg.
- `inventados.tsv`: os 18 números que a IA pôs na tela sem ter dado nenhum, com a linha de cada um.
- `tests/test_30_motion.py`: confere o sha256 do HTML, a moldura, os 18 valores e que o prompt não traz nenhum deles.
- Os HTML entram como `binary` no `.gitattributes` para o sha256 continuar valendo. O MP4 e os quadros ficam no `.gitignore`.
- O README não cita a resposta do chat, que não foi guardada e não tem registro público.

### `19-dicionario` (post 19)
- `gancho.json`: o trecho do gancho, com 3 eventos.
- `skill/SKILL.md`: cópia da skill `programar-post`, sem os ids da conta.
- `mcp-chrome.txt`: os 22 nomes de ferramenta do MCP Claude in Chrome.
- `medir.py`: refaz os números 3, 244, 4.921 e 22 e compara com o `medidas.tsv`.
- `tests/test_19_dicionario.py`.

### Raiz
- `README.md`:
  - linhas 19, 30 e 31 no índice;
  - "Instalar" atualizado com as dependências do 30 e do 31;
  - "Usar" agora fala em cinco pastas com medidor (02, 06, 07, 19 e 31) e explica o que a 30 guarda;
  - nota de que, do post 7 em diante, o número vem do plano de posts e a data pode furar a fila (o 30 sai antes do 7).
- `requirements.txt`: `playwright` comentado, como as outras dependências opcionais (o `gravar.py` também precisa do Google Chrome e do ffmpeg no PATH).
- `CHANGELOG.md`: entrada 0.5.0.

## Como testar

```bash
python -m unittest discover -s tests
```

- [ ] Testes passando no Windows e no Linux (CI)
- [ ] `python 19-dicionario/medir.py` bate com o `medidas.tsv`
- [ ] (opcional) `python 30-motion/gravar.py` gera o MP4 (precisa de Playwright, Chrome e ffmpeg)

Depois do merge, a tag `v0.5.0` vai no commit que publicou a versão.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

Uma coisa a conferir: a linha do README no CHANGELOG cita só o 30, mas o diff também acrescenta o 19 e o 31 ao índice e ao "Usar". Se quiser, corrijo o CHANGELOG ou abro o PR com `gh pr create`.
