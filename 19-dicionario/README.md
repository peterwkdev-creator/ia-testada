# 19-dicionario: hook, skill, MCP e subagente, quem dispara

Medidas do post 19 da @peterwk.dev (a publicar), no pilar Dicionário. As
quatro peças "dão poder" ao Claude Code; o que as separa é **quem
dispara**: o hook roda no evento escolhido, sem o modelo decidir; a skill o
modelo carrega pela descrição; o MCP liga uma ferramenta de fora; o
subagente trabalha num contexto próprio e devolve só o resumo. Cada número
do post é do nosso uso, não regra da ferramenta.

**Medido em 22/10/2026**, no Claude Code (app desktop, Windows).

## Arquivos

- [`gancho.json`](gancho.json): o trecho do nosso `~/.claude/settings.json`
  com os 3 eventos que chamam o `teto-passos.py` (o gancho que conta os
  passos e avisa no 40º). O script não vem junto; o caminho virou `$HOME`.
- [`skill/SKILL.md`](skill/SKILL.md): cópia da nossa skill
  `programar-post`, com os 2 ids da conta Meta trocados por zeros do mesmo
  tamanho.
- [`mcp-chrome.txt`](mcp-chrome.txt): os 22 nomes de ferramenta do MCP
  Claude in Chrome, como a sessão os lista.
- [`medidas.tsv`](medidas.tsv) e [`medir.py`](medir.py): os números e o
  script que refaz os 4 primeiros destes arquivos.

## Refazer

De dentro da raiz do repositório:

```bash
python -I 19-dicionario/medir.py
```

Saída esperada (sai com 1 se algum valor não bater com o `medidas.tsv`):

```
gancho_eventos                    3  ok
skill_descricao_caracteres      244  ok
skill_corpo_caracteres         4921  ok
mcp_chrome_ferramentas           22  ok
```

## Números (22/10/2026)

| Medida | Valor | De onde |
|---|---|---|
| eventos do gancho | 3: UserPromptSubmit, PreToolUse, PostToolUse | `gancho.json` |
| descrição da skill (sempre no contexto) | 244 caracteres | texto depois de `description: ` |
| corpo da skill (só quando é usada) | 4.921 caracteres | o `SKILL.md` depois do topo YAML |
| ferramentas do MCP Claude in Chrome | 22 | `mcp-chrome.txt` |
| subagente que leu a doc deste post | 7 chamadas, 37.900 tokens, 30.739 ms | notificação da tarefa (não se refaz daqui) |
| passo do subagente contra o da sessão | 0,50 | [`07-subagente`](../07-subagente/) |

## Fontes

1. Hooks: https://code.claude.com/docs/en/hooks-guide
2. Skills: https://code.claude.com/docs/en/skills
3. MCP: https://code.claude.com/docs/en/mcp
4. Subagentes: https://code.claude.com/docs/en/sub-agents

## Limites

- Uma máquina, uma conta, uma data. A sua skill, o seu gancho e a sua lista
  de ferramentas dão outros números.
- Só o hook de comando (o nosso) é determinístico: os hooks do tipo prompt
  e agent usam um modelo.
- "Só o resumo" não é custo zero: o resumo do subagente entra no contexto
  da sessão principal.
- O número de ferramentas do Claude in Chrome muda com a versão da extensão.
