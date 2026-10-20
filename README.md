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
| Skill: o que é um SKILL.md e o que não é (a publicar) | medido em 20/10/2026; post previsto para 27/10/2026 | [`06-skill`](06-skill/) | o custo de uma Skill no contexto do Claude Code: a descrição contra o resto do SKILL.md e dos arquivos |
| "Publique seu agente em 5 minutos": no claude.ai, isso não existe (a publicar) | conferido em 20/10/2026; post previsto para 30/10/2026 | [`05-agente`](05-agente/) | se as frases citadas no post ainda estão nas páginas oficiais (Projetos, artefatos, Agent SDK, Managed Agents, preços da API) |

## Como contribuir

Mediu e deu diferente? Abra uma issue pelo modelo "Resultado diferente do
medido", com a data, a versão e a tabela que saiu (sem transcrição nem dado
da conta). Detalhes em [CONTRIBUTING.md](CONTRIBUTING.md); falha de
segurança, em [SECURITY.md](SECURITY.md).

## Licença

[MIT](LICENSE).

## Ferramentas irmãs

- [tts-ptbr](https://github.com/peterwkdev-creator/tts-ptbr): a voz sintética que narra os Reels.
- [carrossel-terminal](https://github.com/peterwkdev-creator/carrossel-terminal): o gerador dos carrosséis e Reels.
- [claude-context-cost](https://github.com/peterwkdev-creator/claude-context-cost): quanto custa o contexto de uma sessão do Claude Code.

<!-- Outros projetos: entra pelo outros-projetos.py da Coordenação -->
