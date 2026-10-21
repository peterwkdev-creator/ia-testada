# ia-testada

As medidas por trás dos posts da [@peterwk.dev](https://www.instagram.com/peterwk.dev/)
(IA testada de verdade, com prova na tela e data): uma pasta por post, com o
script que mediu, a saída dele e um README com a data, a versão do que foi
medido, as fontes, como refazer e os limites. O que se mede é Claude e
Claude Code na prática; este repositório é independente, sem ligação com a
Anthropic.

## Instalar

Python 3.11 ou mais novo, sem dependência fora da biblioteca padrão (nada de
`pip install`):

```bash
git clone https://github.com/peterwkdev-creator/ia-testada.git
cd ia-testada
```

## Usar

Cada pasta do índice abaixo tem o seu medidor e, no README dela, o comando
para refazer a medida. A do post da Skill, por exemplo:

```bash
python -I 06-skill/medir_skills.py <transcrição .jsonl de uma sessão do Claude Code>
```

Os testes dos medidores, com dados inventados:

```bash
python -m unittest -v
```

Cada medida vale para um computador, uma sessão e uma data: a sua pode dar
diferente, e isso é informação.

## Índice

| Post | Data | Pasta | O que mediu |
|---|---|---|---|
| Subagente: o passo custa metade (a publicar) | medido em 21/10/2026 | [`07-subagente`](07-subagente/) | o custo por passo de um subagente contra o da sessão principal, pelo claude-context-cost |
| Skill: o que é um SKILL.md e o que não é (a publicar) | medido em 20/10/2026; post previsto para 27/10/2026 | [`06-skill`](06-skill/) | o custo de uma Skill no contexto do Claude Code: a descrição contra o resto do SKILL.md e dos arquivos |
| "Publique seu agente em 5 minutos": no claude.ai, isso não existe (a publicar) | conferido em 20/10/2026; post previsto para 30/10/2026 | [`05-agente`](05-agente/) | se as frases citadas no post ainda estão nas páginas oficiais (Projetos, artefatos, Agent SDK, Managed Agents, preços da API) |

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
