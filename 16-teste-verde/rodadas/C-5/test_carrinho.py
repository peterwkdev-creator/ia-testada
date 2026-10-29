import unittest

from carrinho import (
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
    def test_limites_validos(self):
        self.assertEqual(validar_quantidade(1), 1)
        self.assertEqual(validar_quantidade(50), 50)
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
        for qtd in (1.0, 2.5, "2", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_lista_vazia(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1000, 2), (250, 3), (99, 1)]), 2849)

    def test_preco_zero(self):
        self.assertEqual(subtotal([(0, 5)]), 0)

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            subtotal([(1000, 1), (-1, 1)])

    def test_quantidade_invalida(self):
        for qtd in (0, QTD_MAXIMA + 1, True, 1.5):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    subtotal([(1000, qtd)])


class TestDesconto(unittest.TestCase):
    def test_sem_cupom(self):
        self.assertEqual(desconto(50000), 0)
        self.assertEqual(desconto(50000, None), 0)

    def test_cupom_desconhecido(self):
        for cupom in ("XYZ", "desc10", ""):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(100, "XYZ")

    def test_desc10_minimo_inclusivo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc20_minimo_inclusivo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_arredonda_para_baixo(self):
        # 10% de 10004 = 1000,4
        self.assertEqual(desconto(10004, "DESC10"), 1000)

    def test_meio_centavo_sobe(self):
        # 10% de 10005 = 1000,5
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredonda_para_cima(self):
        # 10% de 10006 = 1000,6; 20% de 30003 = 6000,6
        self.assertEqual(desconto(10006, "DESC10"), 1001)
        self.assertEqual(desconto(30003, "DESC20"), 6001)


class TestFrete(unittest.TestCase):
    def test_cobra_frete_ate_o_limite_inclusive(self):
        self.assertEqual(frete(0), FRETE)
        self.assertEqual(frete(FRETE_GRATIS_ACIMA), FRETE)

    def test_frete_gratis_acima_do_limite(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA + 1), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_frete(self):
        self.assertEqual(total([]), FRETE)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_com_cupom(self):
        # 15000 - 1500 = 13500, + frete
        self.assertEqual(total([(5000, 3)], "DESC10"), 13500 + FRETE)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + FRETE)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # 22000 daria frete grátis, mas com 10% cai para 19800
        self.assertEqual(total([(22000, 1)]), 22000)
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + FRETE)

    def test_frete_gratis_mesmo_com_desconto(self):
        # 40000 - 8000 = 32000, acima do limite
        self.assertEqual(total([(20000, 2)], "DESC20"), 32000)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(5000, 1)], "XYZ")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
