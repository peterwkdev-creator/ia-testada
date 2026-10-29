import unittest

from carrinho import (
    CUPONS,
    FRETE,
    FRETE_GRATIS_ACIMA,
    QTD_MAXIMA,
    desconto,
    frete,
    subtotal,
    total,
    validar_quantidade,
)


class TestValidarQuantidade(unittest.TestCase):
    def test_devolve_quantidade_valida(self):
        self.assertEqual(validar_quantidade(5), 5)

    def test_limites_inclusivos(self):
        self.assertEqual(validar_quantidade(1), 1)
        self.assertEqual(validar_quantidade(QTD_MAXIMA), QTD_MAXIMA)

    def test_fora_dos_limites(self):
        for qtd in (0, -1, QTD_MAXIMA + 1):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_bool_nao_vale(self):
        for qtd in (True, False):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_tipos_nao_inteiros(self):
        for qtd in (2.0, 1.5, "3", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_sem_itens(self):
        self.assertEqual(subtotal([]), 0)

    def test_um_item(self):
        self.assertEqual(subtotal([(1990, 3)]), 5970)

    def test_varios_itens(self):
        self.assertEqual(subtotal([(1000, 2), (250, 4), (99, 1)]), 3099)

    def test_preco_zero(self):
        self.assertEqual(subtotal([(0, 5), (100, 1)]), 100)

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            subtotal([(1000, 1), (-1, 1)])

    def test_quantidade_invalida(self):
        for qtd in (0, QTD_MAXIMA + 1, True, 1.0):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    subtotal([(1000, qtd)])

    def test_aceita_iteravel_qualquer(self):
        self.assertEqual(subtotal(iter([(100, 2), (50, 1)])), 250)


class TestDesconto(unittest.TestCase):
    def test_sem_cupom(self):
        self.assertEqual(desconto(50000), 0)
        self.assertEqual(desconto(50000, None), 0)

    def test_cupom_desconhecido(self):
        for cupom in ("XYZ", "desc10", "", "DESC10 "):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(0, "XYZ")

    def test_desc10_no_minimo_inclusivo(self):
        _, minimo = CUPONS["DESC10"]
        self.assertEqual(desconto(minimo, "DESC10"), 1000)

    def test_desc10_abaixo_do_minimo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)

    def test_desc20_no_minimo_inclusivo(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_arredondamento_meio_centavo_sobe(self):
        # 10% de 10005 = 1000,5
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredondamento_para_baixo(self):
        # 10% de 10004 = 1000,4
        self.assertEqual(desconto(10004, "DESC10"), 1000)
        # 20% de 30002 = 6000,4
        self.assertEqual(desconto(30002, "DESC20"), 6000)

    def test_arredondamento_para_cima(self):
        # 10% de 10006 = 1000,6
        self.assertEqual(desconto(10006, "DESC10"), 1001)
        # 20% de 30003 = 6000,6
        self.assertEqual(desconto(30003, "DESC20"), 6001)


class TestFrete(unittest.TestCase):
    def test_valor_baixo_paga_frete(self):
        self.assertEqual(frete(0), FRETE)
        self.assertEqual(frete(5000), FRETE)

    def test_no_limite_ainda_paga_frete(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA), FRETE)

    def test_acima_do_limite_frete_gratis(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA + 1), 0)
        self.assertEqual(frete(100000), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_so_frete(self):
        self.assertEqual(total([]), FRETE)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_exatamente_no_limite_paga_frete(self):
        self.assertEqual(total([(10000, 2)]), 20000 + FRETE)

    def test_cupom_aplicado(self):
        # 15000 - 1500 de desconto = 13500, mais frete
        self.assertEqual(total([(15000, 1)], "DESC10"), 13500 + FRETE)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + FRETE)

    def test_frete_calculado_apos_desconto(self):
        # subtotal 22000 teria frete grátis, mas com desconto cai para 19800
        self.assertEqual(total([(11000, 2)], "DESC10"), 19800 + FRETE)

    def test_frete_gratis_apos_desconto(self):
        # 40000 - 8000 = 32000, acima do limite
        self.assertEqual(total([(10000, 4)], "DESC20"), 32000)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(10000, 1)], "XYZ")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
