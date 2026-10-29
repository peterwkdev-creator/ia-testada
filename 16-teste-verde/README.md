# 16-teste-verde: os testes que o Claude Code escreve pegam defeito?

Medida do post 16 da @peterwk.dev (a publicar), no pilar Corrigido: pedimos
ao Claude Code os testes de unidade de um módulo pequeno, 5 vezes em cada uma
de três condições, e conferimos as 15 suítes contra **10 defeitos plantados**
de uma linha. Verificador que não pega o defeito plantado não vale; teste
verde com código quebrado é o risco.

**Medido em 29/10/2026, com o Claude Code 2.1.309 no modelo padrão (saiu
`claude-opus-5-5` nas 15 rodadas)**, no Windows, com Python 3.12.

Resultado: **as 15 suítes ficaram verdes no código certo e pegaram os 10
defeitos, nas três condições** (10 de 10, mínimo e máximo), inclusive na C,
em que as docstrings não traziam os exemplos de fronteira. A margem é que
é estreita: o defeito do brinde recusado (`d08`) caiu por **um teste só**
nas 15 suítes, e o do meio centavo (`d05`), em 12 das 15. Apague esse teste
e a suíte continua verde com o código quebrado.

## O que mede

O módulo é [`projeto/carrinho.py`](projeto/carrinho.py) (subtotal, cupom com
valor mínimo, frete grátis acima de R$ 200,00, desconto arredondado em
centavos com meio centavo para cima, validação de quantidade), com a regra
nas docstrings e sem testes. Cada rodada copia **só** a pasta `projeto/`
para uma pasta temporária nova e roda uma vez, no modelo padrão:

```
A: claude -p "Escreva os testes de unidade de carrinho.py em test_carrinho.py, com unittest."
B: a mesma frase + "Antes de terminar, prove que os testes pegam defeito:
   plante um erro no código, veja um teste falhar e desfaça."
C: a frase da A, sobre projeto-c/carrinho.py
```

A [`projeto-c/carrinho.py`](projeto-c/carrinho.py) da condição C é o mesmo
código com as docstrings sem os exemplos de fronteira: a regra continua em
palavras ("inclusive", "passa de", "meio centavo sobe"), mas saíram o
"R$ 100,05 com 10% dá R$ 10,01", o "R$ 200,00 exatos ainda pagam frete", o
"Preço 0 vale (brinde)" e o "R$ 12,34 = 1234". O teste do repositório
confere, pela árvore sintática sem as docstrings (`sem_docstrings`), que o
código é idêntico ao do certo, e que os defeitos de
[`defeitos-c/`](defeitos-c/) são os mesmos 10 de `defeitos/`.

com Read, Write, Edit, Glob, Grep e Bash liberado só para `python`, sem
guardar a sessão, sem os ganchos do usuário e sem o `CLAUDE.md` global
(`claudeMdExcludes`). Depois, o `carrinho.py` da pasta temporária se confere
pelo sha256 (nas 10 rodadas saiu igual ao original; a contagem usa sempre o
original).

Os defeitos ficam em [`defeitos/`](defeitos/), cada um o `carrinho.py` com
uma linha trocada:

| Defeito | O que muda |
|---|---|
| `d01_frete_fronteira` | frete grátis em `>=` R$ 200,00, não só acima |
| `d02_cupom_fronteira` | cupom só vale acima do mínimo, não no mínimo |
| `d03_qtd_maxima` | quantidade 99 recusada (off-by-one) |
| `d04_qtd_zero` | quantidade 0 aceita |
| `d05_meio_centavo` | meio centavo arredonda para baixo |
| `d06_frete_antes_do_desconto` | frete calculado sobre o subtotal, antes do cupom |
| `d07_cupom_desconhecido` | cupom desconhecido dá desconto 0 em vez de erro |
| `d08_brinde_recusado` | item de preço 0 dá erro |
| `d09_minimo_desc20` | mínimo do DESC20 cai de R$ 300,00 para R$ 200,00 |
| `d10_trunca_centavo` | desconto truncado, sem arredondar |

A prova de que os 10 são matáveis é a [`referencia_test.py`](referencia_test.py):
passa no certo e falha em cada defeito (o teste do repositório confere). Ela
e os defeitos nunca entram na pasta da rodada.

## Pré-requisitos

- Python 3.11 ou mais novo (só a biblioteca padrão).
- O Claude Code com login (cada rodada custou de US$ 0,17 a 0,50).

## Passo a passo

De dentro desta pasta (`cd 16-teste-verde`):

```bash
python -I medir_teste_verde.py rodar 5
python -I medir_teste_verde.py contar
```

O `rodar` grava `rodadas/A-N/` e `rodadas/B-N/`: o `test_carrinho.py`
gerado e o `numeros.json` (modelo, turnos, duração, custo e tokens; nenhum
texto da sessão). Rodada já gravada não se refaz. O `contar` roda cada
suíte no certo e nos 10 defeitos (pegou = algum teste falha ou dá erro;
suíte que não fica verde no certo não conta como "pegou") e grava o
[`medidas.tsv`](medidas.tsv) (uma linha por rodada, o resumo no rodapé) e o
[`defeitos.tsv`](defeitos.tsv) (rodada × defeito, com quantos testes caíram).

## Números (29/10/2026)

| Rodada | Turnos | Duração (s) | Tokens | US$ | Testes | Verde no certo | Defeitos pegos |
|---|---|---|---|---|---|---|---|
| A-1 | 4 | 38,2 | 142.051 | 0,42 | 27 | sim | 10 de 10 |
| A-2 | 4 | 41,0 | 142.366 | 0,43 | 25 | sim | 10 de 10 |
| A-3 | 6 | 38,7 | 210.557 | 0,20 | 36 | sim | 10 de 10 |
| A-4 | 4 | 45,5 | 142.520 | 0,43 | 33 | sim | 10 de 10 |
| A-5 | 5 | 36,2 | 141.944 | 0,42 | 28 | sim | 10 de 10 |
| B-1 | 10 | 40,8 | 303.658 | 0,50 | 26 | sim | 10 de 10 |
| B-2 | 10 | 81,5 | 280.423 | 0,49 | 29 | sim | 10 de 10 |
| B-3 | 9 | 41,9 | 231.927 | 0,45 | 26 | sim | 10 de 10 |
| B-4 | 8 | 74,3 | 312.280 | 0,29 | 31 | sim | 10 de 10 |
| B-5 | 10 | 49,8 | 308.809 | 0,25 | 39 | sim | 10 de 10 |
| C-1 | 4 | 47,7 | 141.477 | 0,42 | 31 | sim | 10 de 10 |
| C-2 | 4 | 39,9 | 143.153 | 0,43 | 33 | sim | 10 de 10 |
| C-3 | 4 | 36,3 | 170.303 | 0,18 | 35 | sim | 10 de 10 |
| C-4 | 6 | 44,1 | 144.321 | 0,45 | 28 | sim | 10 de 10 |
| C-5 | 4 | 35,8 | 169.563 | 0,17 | 28 | sim | 10 de 10 |

Tokens = entrada (com cache) + saída.

| | A | B | C |
|---|---|---|---|
| Defeitos pegos (mín.–máx., mediana) | 10–10, 10 | 10–10, 10 | 10–10, 10 |
| Suítes verdes no certo | 5 de 5 | 5 de 5 | 5 de 5 |
| Testes por suíte | 25–36, mediana 28 | 26–39, mediana 29 | 28–35, mediana 31 |
| Tokens | 141.944–210.557, mediana 142.366 | 231.927–312.280, mediana 303.658 | 141.477–170.303, mediana 144.321 |
| Custo total | US$ 1,89 | US$ 1,97 | US$ 1,65 |

Pedir a prova (B) dobrou os turnos (4–6 contra 8–10) e subiu a mediana de
tokens em 2,1×, sem mudar o placar, que já era 10 de 10 em A. Tirar os
exemplos das docstrings (C) também não mudou o placar.

Quantos testes caíram com cada defeito (mínimo–máximo nas 15 suítes):
`d01` 1–4, `d02` 2–4, `d03` 1–2, `d04` 2–3, `d05` 1–2, `d06` 1–2, `d07` 2–6,
`d08` 1–1, `d09` 1–2, `d10` 1–3 (por condição, no rodapé do `medidas.tsv`).
O `d08` caiu por um teste só nas 15; o `d05`, em 12 das 15 (5 na A, 4 na B,
3 na C). Na A-1, o `d05` só cai em `test_arredonda_meio_centavo_para_cima`
(1000 != 1001), e o `d08` só em `test_brinde_de_preco_zero`. Na C-3, sem os
exemplos no texto, os únicos são `test_arredondamento_meio_centavo_sobe` e
`test_preco_zero`.

## Limites

- Um módulo só, pequeno, com a regra escrita nas docstrings (na C, sem os
  exemplos, mas ainda em palavras). Com a regra só no código, ou num módulo
  maior, o resultado pode ser outro.
- Uma frase por condição, uma máquina, 5 rodadas em cada.
- 10 defeitos escolhidos por nós, de uma linha; não é análise de mutação
  completa.
- O modelo padrão muda com a conta e com a versão do Claude Code.
