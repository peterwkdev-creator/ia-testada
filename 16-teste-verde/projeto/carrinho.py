"""Carrinho de compras de uma loja pequena: subtotal, cupom, frete e total.

Todos os valores são inteiros em centavos (R$ 12,34 = 1234).
"""

FRETE = 1500  # R$ 15,00
FRETE_GRATIS_ACIMA = 20000  # frete grátis quando o valor passa de R$ 200,00
QTD_MAXIMA = 99
# cupom: (percentual de desconto, subtotal mínimo em centavos, inclusive)
CUPONS = {"DESC10": (10, 10000), "DESC20": (20, 30000)}


def validar_quantidade(qtd):
    """Devolve qtd se for um int de 1 a QTD_MAXIMA, inclusive; senão, ValueError.

    bool não vale como quantidade."""
    if isinstance(qtd, bool) or not isinstance(qtd, int):
        raise ValueError("a quantidade deve ser um número inteiro")
    if qtd < 1 or qtd > QTD_MAXIMA:
        raise ValueError(f"quantidade fora de 1 a {QTD_MAXIMA}: {qtd}")
    return qtd


def subtotal(itens):
    """Soma de preço × quantidade de cada item (preco_em_centavos, qtd).

    Preço 0 vale (brinde); preço negativo dá ValueError."""
    soma = 0
    for preco, qtd in itens:
        if preco < 0:
            raise ValueError(f"preço negativo: {preco}")
        soma += preco * validar_quantidade(qtd)
    return soma


def desconto(valor, cupom=None):
    """Desconto do cupom sobre valor, em centavos.

    O cupom só vale com valor maior ou igual ao mínimo dele; abaixo, o
    desconto é 0. Sem cupom, 0. Cupom desconhecido: ValueError. O desconto se
    arredonda para o centavo mais próximo, e meio centavo sobe
    (R$ 100,05 com 10% dá R$ 10,01)."""
    if cupom is None:
        return 0
    if cupom not in CUPONS:
        raise ValueError(f"cupom desconhecido: {cupom}")
    percentual, minimo = CUPONS[cupom]
    if valor < minimo:
        return 0
    return (valor * percentual + 50) // 100


def frete(valor):
    """Frete do pedido: 0 se valor passa de FRETE_GRATIS_ACIMA; senão, FRETE.

    R$ 200,00 exatos ainda pagam frete."""
    if valor > FRETE_GRATIS_ACIMA:
        return 0
    return FRETE


def total(itens, cupom=None):
    """Subtotal menos o desconto do cupom, mais o frete.

    O frete se calcula sobre o valor já com desconto."""
    sub = subtotal(itens)
    com_desconto = sub - desconto(sub, cupom)
    return com_desconto + frete(com_desconto)
