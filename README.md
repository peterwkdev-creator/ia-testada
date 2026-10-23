# ia-testada

As medidas por trás dos posts da [@peterwk.dev](https://www.instagram.com/peterwk.dev/)
(IA testada de verdade, com prova na tela e data). Cada post tem um número.
Quando há o que refazer, há uma pasta numerada, com o script que mediu, a
saída dele e um README com a data, a versão do que foi medido, as fontes,
como refazer e os limites. O índice abaixo liga cada post à sua pasta. O que se mede é Claude e
Claude Code na prática; este repositório é independente, sem ligação com a
Anthropic.

**Antes de começar:** nunca rodou um script em Python? Comece pelo
[GUIA](GUIA.md): instalar o Python, baixar o repositório, rodar os testes,
achar uma transcrição sua e rodar um medidor, passo a passo, no Windows, no
macOS e no Linux.

## Instalar

Python 3.11 ou mais novo. Tudo usa só a biblioteca padrão, menos o 07 e o 31
(`claude-context-cost`), o `capturar.py` do 05 (`websockets` e o Google
Chrome) e o `gravar.py` do 30 (`playwright`, o Google Chrome e o ffmpeg);
essas dependências opcionais estão no
[`requirements.txt`](requirements.txt). Os testes não precisam de nenhuma.

```bash
git clone https://github.com/peterwkdev-creator/ia-testada.git
cd ia-testada
```

No Windows, onde estiver `python`, `py` também serve.

## Usar

Cinco pastas têm medidor: a 02, a 06, a 07, a 19 e a 31. A 05 tem um conferidor de
fontes e o script das capturas de tela; a 04 aponta para o código no
tts-ptbr; a 30 guarda um prompt testado, o HTML que ele deu e o gravador
que o põe em MP4. Cada README traz o passo a passo para refazer. O medidor do post
da Skill, por exemplo:

```bash
python -I 06-skill/medir_skills.py <transcrição .jsonl de uma sessão do Claude Code>
```

E a do post 2 (onde vão os tokens de uma sessão):

```bash
python -I 02-releitura/medir_sessao.py <transcrição .jsonl de uma sessão do Claude Code>
```

Os testes dos medidores, com dados inventados:

```bash
python -m unittest -v
```

Cada medida vale para um computador, uma sessão e uma data: a sua pode dar
diferente, e isso é informação.

## Índice

"Post nº" é o número do post, na ordem de publicação. A pasta, quando
existe, tem o mesmo número, com uma exceção: os posts 5 e 6 trocaram de
data em 20/10/2026, e as pastas não mudaram de nome (os links das
legendas apontam para elas). Por isso a pasta `05-agente` é o post 6, e a `06-skill`, o
post 5. Os posts 1 e 3 não têm pasta. Do 7 em diante, o número é
o do plano de posts, e a data de publicação pode furar a fila: o 30 sai
antes do 7.

| Post nº | Post | Data | Onde está o código | O que mediu |
|---|---|---|---|---|
| 1 | Agente de IA com Claude: conferi no claude.ai e no Claude Code o que existe de verdade. | publicado em 18/10/2026 | sem pasta: leitura de páginas oficiais, sem script | o que existe para montar agente (Projetos, Skills e o resto), conferido peça por peça nas páginas oficiais e na conta |
| 2 | Claude Code: 96% dos tokens de uma sessão são o Claude relendo a conversa | medido em 29/09 e 18/10/2026; publicado em 19/10/2026 | [`02-releitura`](02-releitura/) | releitura, gravação de cache e saída de uma sessão, pela transcrição |
| 3 | Como fizemos a nossa voz (TTS v1) | publicado em 21/10/2026 | sem pasta: no [tts-ptbr](https://github.com/peterwkdev-creator/tts-ptbr) | a voz sintética dos Reels: modelo aberto, normalizador e dicionário nossos |
| 4 | 6 vozes abertas leem a mesma frase | medido em 19/10/2026; post previsto para 23/10/2026 | [`04-vozes`](04-vozes/), que aponta para o `tts-ptbr/exemplos` | quantas palavras cada uma de 6 vozes abertas errou, pelo Whisper |
| 5 | Skill: o que é um SKILL.md e o que não é (a publicar) | medido em 20/10/2026; post previsto para 27/10/2026 | [`06-skill`](06-skill/) (pasta 06) | o custo de uma Skill no contexto do Claude Code: a descrição contra o resto do SKILL.md e dos arquivos |
| 6 | "Publique seu agente em 5 minutos": no claude.ai, isso não existe (a publicar) | conferido em 20/10/2026; post previsto para 30/10/2026 | [`05-agente`](05-agente/) (pasta 05) | se as frases citadas no post ainda estão nas páginas oficiais (Projetos, artefatos, Agent SDK, Managed Agents, preços da API) |
| 7 | Subagente: o passo custa metade (a publicar) | medido em 21/10/2026 | [`07-subagente`](07-subagente/) | o custo por passo de um subagente contra o da sessão principal, pelo claude-context-cost |
| 19 | Hook, Skill, MCP e subagente: quem dispara? (a publicar) | medido em 22/10/2026; post previsto para 06/11/2026 | [`19-dicionario`](19-dicionario/) | os números do post nos nossos arquivos: 3 eventos do gancho, 244 caracteres de descrição contra 4.921 de corpo numa skill, 22 ferramentas do MCP do Chrome |
| 30 | O prompt de motion que viralizou, testado (a publicar) | testado em 21/10/2026; post previsto para 28/10/2026 | [`30-motion`](30-motion/) | se o prompt sai de primeira no claude.ai, quais números a IA inventou na tela (18) e o passo do HTML ao MP4 |
| 31 | Agent Teams: 3 agentes em time custaram 4× uma sessão só (a publicar) | medido em 23/10/2026; post previsto para 10/11/2026 | [`31-agent-teams`](31-agent-teams/) | a mesma tarefa feita por uma sessão só e por um líder com 3 teammates: 141.260 contra 564.642 tokens, pelo claude-context-cost |

## Como contribuir

Mediu e deu diferente? Abra uma issue pelo modelo "Resultado diferente do
medido", com a data, a versão e a tabela que saiu (sem transcrição nem dado
da conta). Detalhes em [CONTRIBUTING.md](CONTRIBUTING.md); falha de
segurança, em [SECURITY.md](SECURITY.md).

<!-- outros-projetos:inicio -->
## Outros projetos

| Projeto | Para que serve |
|---|---|
| [numeros-publicos](https://github.com/peterwkdev-creator/numeros-publicos) · [site](https://www.numerospublicos.com.br) | Dados abertos de cada município brasileiro (IBGE, Tesouro Nacional, INEP), conferidos contra a fonte, uma página por município |
| [simples-nacional-br](https://github.com/peterwkdev-creator/simples-nacional-br) · [site](https://peterwkdev-creator.github.io/simples-nacional-br/) | Simples Nacional conferido contra a LC 123 e a LC 214: alíquota, DAS, repartição, Fator R e CNAE |
| [linguagem-simples-br](https://github.com/peterwkdev-creator/linguagem-simples-br) · [site](https://peterwkdev-creator.github.io/linguagem-simples-br/) | Verificador aberto da Lei 15.263/2025 (Linguagem Simples): confere um texto contra o art. 5º |
| [claude-context-cost](https://github.com/peterwkdev-creator/claude-context-cost) · [site](https://peterwkdev-creator.github.io/claude-context-cost/) | Quanto cada fonte (CLAUDE.md, regras, skills, memória) custa no contexto de uma sessão do Claude Code |
| [vra-anac](https://github.com/peterwkdev-creator/vra-anac) | Pontualidade dos voos domésticos do Brasil pelo VRA da ANAC |
| [tts-ptbr](https://github.com/peterwkdev-creator/tts-ptbr) | Voz sintética em português com modelos abertos (Kokoro e Piper), medida pelo Whisper |
| [carrossel-terminal](https://github.com/peterwkdev-creator/carrossel-terminal) | Carrossel do Instagram no visual de terminal: Markdown vira PNG, conferido antes de publicar, e o post vira Reel |
| [numerasheets-site](https://github.com/peterwkdev-creator/numerasheets-site) · [site](https://numerasheets.com) | Vitrine da loja NumeraSheets: modelos de planilha e calculadoras grátis |
<!-- outros-projetos:fim -->

## Licença

[MIT](LICENSE).
