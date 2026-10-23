# 31-agent-teams: quanto custa um time de agentes

Medida do post sobre Agent Teams da @peterwk.dev (a publicar), no pilar
Medido: a mesma tarefa feita por uma sessão só e por um líder com 3
teammates. O time custou **4,0 vezes** mais, com o mesmo resultado (todos
os testes passando).

**Medido em 23/10/2026, com o Claude Code 2.1.308 (`--model sonnet`) e o
claude-context-cost v1.6.4**, no Windows.

## O que mede

Cada resposta do modelo relê o contexto inteiro da conversa; é esse
contexto, contado pelo uso da API gravado na transcrição, que se soma aqui.
O `medir_time.py` soma, de cada lado:

1. **solo:** a sessão que fez a tarefa sozinha;
2. **time:** a sessão do líder mais a de cada teammate (o Claude Code grava
   o teammate como subagente do líder, em
   `<sessão do líder>/subagents/*.jsonl`).

E divide um pelo outro. Não conta tokens por conta própria: chama o
[claude-context-cost](https://github.com/peterwkdev-creator/claude-context-cost)
com `--json` nas duas pastas.

## Pré-requisitos

- Python 3.11 ou mais novo.
- `pip install claude-context-cost` (1.6.3 ou mais novo).
- Claude Code com Agent Teams (recurso experimental, 2.1.308 na medida).

## Passo a passo

1. Crie duas pastas vazias, `solo` e `time`, e copie o
   [`TAREFA.md`](TAREFA.md) para as duas.
2. Na `time`, ligue o recurso **só nela**: copie o
   [`settings-time.json`](settings-time.json) para
   `time/.claude/settings.local.json`. Ligado no global, todo subagente
   nomeado vira teammate em todas as sessões.
3. Abra o Claude Code interativo em cada pasta (em `-p` não há teammates),
   com `claude --model sonnet`, e digite:
   - no `solo`: `Leia TAREFA.md e faca a tarefa sozinho, sem subagentes.`
   - no `time`: `Leia TAREFA.md. Crie um agent team com 3 teammates Sonnet,
     um para cada modulo (um dono por arquivo). Voce so coordena e roda
     python -m unittest no fim.`
4. Quando os dois terminarem, ache as pastas das transcrições: no Windows,
   `%USERPROFILE%\.claude\projects\<pasta do projeto>` (no macOS e no
   Linux, `~/.claude/projects/<pasta do projeto>`), uma por projeto. E
   rode, de dentro desta pasta (`cd 31-agent-teams`):

   ```bash
   pip install claude-context-cost
   python -I medir_time.py <pasta do solo> <pasta do time>
   ```

As transcrições são suas e têm dado da conta: não as publique nem as cole
em issue. O `.gitignore` deste repositório barra `*.jsonl`.

## Saída esperada

Uma tabela `medida`/`valor` na tela, a mesma que vai para o
[`medidas.tsv`](medidas.tsv) desta pasta: respostas e tokens do solo, do
líder, dos teammates (somados e um a um, pelo nome que a tarefa deu a cada
um) e do time inteiro, e a razão time ÷ solo. Só contagens: nenhum nome de
arquivo, id de sessão ou texto da conversa. O
script para com uma mensagem se o solo tiver subagentes, se o time não
tiver teammates ou se as duas pastas forem medidas com versões diferentes
do claude-context-cost.

## Números (23/10/2026)

| Medida | Solo | Time |
|---|---|---|
| contextos | 1 | 4 (líder + 3 teammates) |
| respostas | 4 | 17 (líder 6, teammates 11) |
| tokens | 141.260 | 564.642 (líder 218.228, teammates 346.414) |
| por teammate | | cpf 127.088 (4 respostas), temperatura 93.365 (3), palavras 125.961 (4) |
| razão time ÷ solo | | **4,0** |
| testes passando | 8 | 15 |

Bate com a documentação oficial
([code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams)),
que diz que o custo cresce linearmente com os teammates: 4 contextos, 4
vezes o custo.

## Limites

- Uma rodada de cada lado: amostra de 1.
- Tarefa pequena, que uma sessão só fazia sem dificuldade; numa tarefa que
  não cabe num contexto, a conta pode mudar.
- O time escreveu 15 testes e o solo 8: o resultado foi o mesmo (tudo
  passando), o trabalho não foi idêntico.
- A aba do time abriu em modo auto e a do solo em `acceptEdits`; os
  diálogos de abertura (confiança na pasta) foram respondidos à mão nas
  duas.
- O `settings-time.json` daqui é o da rodada sem uma permissão de comando
  que a sessão pediu durante a tarefa.
- Caminho longo no Windows: o claude-context-cost 1.6.4 falha com
  `WinError 3` quando o caminho do teammate passa de 260 caracteres. O
  script contorna copiando cada pasta para uma pasta temporária curta antes
  de medir.
