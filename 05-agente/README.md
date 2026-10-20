# 05-agente: "publique seu agente em 5 minutos" no claude.ai

Prova do post "'Publique seu agente em 5 minutos': no claude.ai, isso não
existe" da @peterwk.dev (a publicar; previsto para 30/10/2026).

**Conferido em 20/10/2026**, nas páginas oficiais abaixo.

## O que confere

O post não mede um número: ele cita páginas oficiais. Página de documentação
muda sem aviso (a do Managed Agents ganhou "scheduled deployments" entre 18 e
20/10/2026). O `conferir_fontes.py` baixa cada página e confere, frase a
frase, se o trecho citado no post ainda está lá. A saída vai para o
[`conferencia.tsv`](conferencia.tsv) desta pasta, com a data e a hora da
leitura (UTC), e o script sai com código 1 se alguma frase sumiu.

## Como refazer

```bash
python -I conferir_fontes.py
```

Só a biblioteca padrão do Python; precisa de rede. Não lê nada da sua conta.

## A afirmação e o limite dela

No claude.ai não há como publicar um agente como app ou bot para o público:

- o Projeto do chat só se compartilha dentro da organização, nos planos Team
  e Enterprise;
- o que se compartilha é o artefato, e quem o usa gasta o próprio plano;
- um agente que roda para outras pessoas existe, mas pela API (Agent SDK ou
  Managed Agents), com chave de API e cobrança por uso.

Vale para o claude.ai e para as páginas lidas na data da conferência. Não
dizemos que "não existe agente publicável": pela API, existe.

## Fontes (lidas em 20/10/2026)

1. Compartilhar Projeto (Central de Ajuda):
   https://support.claude.com/en/articles/9519189-manage-project-visibility-and-sharing
2. Artefatos (Central de Ajuda):
   https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them
3. Agent SDK, overview: https://code.claude.com/docs/en/agent-sdk/overview
4. Managed Agents, overview (beta): https://platform.claude.com/docs/en/managed-agents/overview
5. Projects do Claude Code (para não confundir com os do chat):
   https://code.claude.com/docs/en/claude-projects
6. Preços da API (a "cobrança por uso": tokens e, no Managed Agents, tempo
   de sessão): https://platform.claude.com/docs/en/about-claude/pricing

## Limites

- A frase estar na página não diz que nada mudou em volta dela: o script
  confere o trecho citado, não a página inteira.
- A afirmação central é uma ausência ("não há opção de publicar"), e frase
  presente não prova ausência: se um botão de publicar surgir, o script não
  vê. Essa parte vale pela leitura das páginas na data acima.
- A Central de Ajuda não traz data de atualização ("Updated over a week
  ago"): o que vale é a data da leitura.
- Os planos Team e Enterprise não foram conferidos por dentro; o que se diz
  deles vem da página 1.
