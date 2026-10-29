import unittest

from carrinho import (
    FRETE,
    QTD_MAXIMA,
    desconto,
    frete,
    subtotal,
    total,
    validar_quantidade,
)


class TestValidarQuantidade(unittest.TestCase):
    def test_devolve_a_quantidade_valida(self):
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

    def test_nao_inteiro(self):
        for qtd in (1.0, 2.5, "3", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1000, 2), (250, 3)]), 2750)

    def test_preco_zero(self):
        self.assertEqual(subtotal([(0, 5), (100, 1)]), 100)

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

    def test_cupom_desconhecido_mesmo_abaixo_do_minimo(self):
        with self.assertRaises(ValueError):
            desconto(0, "XYZ")

    def test_desc10(self):
        self.assertEqual(desconto(15000, "DESC10"), 1500)

    def test_desc20(self):
        self.assertEqual(desconto(40000, "DESC20"), 8000)

    def test_minimo_inclusivo(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_abaixo_do_minimo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_arredondamento(self):
        self.assertEqual(desconto(10004, "DESC10"), 1000)  # 1000,4
        self.assertEqual(desconto(10006, "DESC10"), 1001)  # 1000,6
        self.assertEqual(desconto(30003, "DESC20"), 6001)  # 6000,6

    def test_meio_centavo_sobe(self):
        self.assertEqual(desconto(10005, "DESC10"), 1001)  # 1000,5
        self.assertEqual(desconto(10015, "DESC10"), 1002)  # 1001,5


class TestFrete(unittest.TestCase):
    def test_cobra_frete(self):
        self.assertEqual(frete(0), FRETE)
        self.assertEqual(frete(10000), FRETE)

    def test_limite_nao_e_gratis(self):
        self.assertEqual(frete(20000), FRETE)

    def test_gratis_acima_do_limite(self):
        self.assertEqual(frete(20001), 0)
        self.assertEqual(frete(50000), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_frete(self):
        self.assertEqual(total([]), FRETE)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(21000, 1)]), 21000)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9000, 1)], "DESC10"), 9000 + FRETE)

    def test_frete_sobre_valor_com_desconto(self):
        # 21000 passa do limite, mas com 10% vira 18900 e volta a pagar frete
        self.assertEqual(total([(21000, 1)], "DESC10"), 18900 + FRETE)

    def test_desconto_e_frete_gratis(self):
        self.assertEqual(total([(10000, 3)], "DESC20"), 24000)

    def test_varios_itens_com_arredondamento(self):
        # subtotal 10005; desconto 1001 (1000,5 sobe); 9004 + frete
        self.assertEqual(total([(10000, 1), (5, 1)], "DESC10"), 9004 + FRETE)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(1000, 1)], "XYZ")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
