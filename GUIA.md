# Guia: do zero à sua primeira medida

Para quem nunca rodou um script em Python. Leva uns 10 minutos. Escrito em
21/10/2026; cada pasta tem o README dela com o detalhe. Palavras como
issue, PATH, clone e cache estão explicadas no [glossário](#glossário), no
fim.

## 1. Instale o Python (3.11 ou mais novo)

Confira se já tem, num terminal (PowerShell no Windows; Terminal no macOS e
no Linux):

```bash
python --version
```

- **Windows:** se o comando não existir ou abrir a Microsoft Store, instale
  pelo https://www.python.org/downloads/ e marque "Add python.exe to PATH".
  O instalador também traz o `py`: `py --version` funciona mesmo sem o PATH.
  Neste guia, onde estiver `python`, você pode usar `py`.
- **macOS e Linux:** o comando costuma ser `python3`. Onde estiver `python`,
  use `python3`.

A versão precisa ser 3.11 ou mais nova (`Python 3.11.x`, `3.12.x`...).

## 2. Baixe o repositório

Com o Git:

```bash
git clone https://github.com/peterwkdev-creator/ia-testada.git
cd ia-testada
```

Sem o Git: na página do repositório, "Code" > "Download ZIP", descompacte e
abra o terminal dentro da pasta `ia-testada`.

## 3. Rode os testes

```bash
python -m unittest -v
```

Os testes usam dados inventados: não leem nada seu. No fim deve aparecer
`OK` (um teste fica `skipped`: ele só roda numa transcrição sua, se você
pedir; veja o README do `02-releitura`). Se aparecer `FAILED`, abra uma
issue com a saída.

## 4. Ache uma transcrição sua

Cada sessão do Claude Code fica gravada num arquivo `.jsonl` (um JSON por
linha), uma pasta por projeto:

| Sistema | Onde |
|---|---|
| Windows | `%USERPROFILE%\.claude\projects\<pasta do projeto>\<id da sessão>.jsonl` |
| macOS e Linux | `~/.claude/projects/<pasta do projeto>/<id da sessão>.jsonl` |

O nome da pasta do projeto é o caminho dele com `:`, `\` e `/` trocados por
`-`. A transcrição mais recente (fora da pasta `subagents`, onde ficam as
transcrições dos subagentes, `agent-*.jsonl`):

- Windows (PowerShell):

  ```powershell
  Get-ChildItem "$env:USERPROFILE\.claude\projects" -Recurse -Filter *.jsonl |
    Where-Object { $_.FullName -notmatch '\\subagents\\' } |
    Sort-Object LastWriteTime | Select-Object -Last 1 -ExpandProperty FullName
  ```

- macOS e Linux:

  ```bash
  ls -t ~/.claude/projects/*/*.jsonl | head -1
  ```

  (Este só olha um nível abaixo de cada projeto: a pasta `subagents` já
  fica de fora.)

**A transcrição é sua e tem dado da conta** (o que você escreveu, o que o
Claude leu, caminhos do seu computador). Não a publique, não a cole numa
issue e não a ponha neste repositório: o `.gitignore` barra `*.jsonl`, mas
o cuidado é seu.

## 5. Rode um medidor

O do post da Skill (`06-skill`) só precisa da transcrição. Entre na pasta e
passe o caminho entre aspas:

```bash
cd 06-skill
python -I medir_skills.py "<caminho da transcrição .jsonl>"
```

O `-I` roda o script isolado: o Python não carrega módulos da pasta atual
nem lê as variáveis `PYTHON*` do ambiente. O do post 2 é parecido:
`python -I medir_sessao.py "<caminho>"`, dentro de `02-releitura`.

## 6. Leia a saída

Cada medidor imprime uma tabela na tela. O README da pasta diz, em "Saída
esperada" e "Como ler", o que é cada coluna, e em "Números" traz a medida
do post, com a data. Compare a sua com a de lá:

- deu parecido: a medida se repete no seu computador;
- deu diferente: isso é informação. Outra versão do Claude Code, outras
  skills ou outra sessão mudam o número. Se quiser contar, abra uma issue
  pelo modelo "Resultado diferente do medido", com a data, a versão e a
  tabela que saiu, **sem a transcrição**.

## 7. Os que pedem instalação

Quase tudo aqui usa só a biblioteca padrão do Python. As exceções estão no
[`requirements.txt`](requirements.txt):

- `07-subagente`: `pip install claude-context-cost`;
- `05-agente/capturar.py`: `pip install websockets` e o Google Chrome.

No Windows, se `pip` não existir, use `py -m pip install ...`.

## Glossário

- **issue:** um aviso aberto na aba "Issues" do repositório no GitHub, para
  contar um erro ou um resultado diferente.
- **PATH:** a lista de pastas onde o sistema procura os programas; com o
  Python no PATH, o comando `python` funciona em qualquer pasta.
- **clone:** a cópia do repositório inteiro no seu computador, feita pelo
  `git clone`.
- **cache:** a parte da conversa que o Claude já leu e guarda para reler
  mais barato na resposta seguinte.
- **mediana:** o valor do meio quando os números são postos em ordem; metade
  fica abaixo, metade acima.
- **p90:** o valor abaixo do qual ficam 90% dos números.
- **Whisper:** um modelo aberto que transcreve áudio em texto; aqui, ele
  confere o que as vozes sintéticas falaram.
- **YAML:** um formato de texto para dados (`chave: valor`); é o topo de um
  `SKILL.md`, entre linhas `---`.
