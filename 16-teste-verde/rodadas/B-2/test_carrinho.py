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
    def test_limites_validos(self):
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
        for qtd in (1.0, "1", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1234, 2), (500, 3)]), 1234 * 2 + 500 * 3)

    def test_brinde_preco_zero(self):
        self.assertEqual(subtotal([(0, 5), (1000, 1)]), 1000)

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            subtotal([(1000, 1), (-1, 1)])

    def test_quantidade_invalida(self):
        for qtd in (0, QTD_MAXIMA + 1, True, 2.0):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    subtotal([(1000, qtd)])


class TestDesconto(unittest.TestCase):
    def test_sem_cupom(self):
        self.assertEqual(desconto(50000), 0)
        self.assertEqual(desconto(50000, None), 0)

    def test_cupom_desconhecido(self):
        for cupom in ("XPTO", "desc10", ""):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(1, "XPTO")

    def test_desc10_no_minimo_vale(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc10_abaixo_do_minimo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)

    def test_desc20_no_minimo_vale(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_meio_centavo_arredonda_para_cima(self):
        # R$ 100,05 com 10% = 1000,5 centavos -> 1001
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredonda_para_baixo_abaixo_do_meio(self):
        # 1000,4 centavos -> 1000
        self.assertEqual(desconto(10004, "DESC10"), 1000)

    def test_arredonda_para_cima_acima_do_meio(self):
        # 1000,6 centavos -> 1001
        self.assertEqual(desconto(10006, "DESC10"), 1001)


class TestFrete(unittest.TestCase):
    def test_duzentos_reais_exatos_paga_frete(self):
        self.assertEqual(frete(20000), FRETE)

    def test_acima_de_duzentos_frete_gratis(self):
        self.assertEqual(frete(20001), 0)

    def test_valor_baixo_paga_frete(self):
        self.assertEqual(frete(0), FRETE)
        self.assertEqual(frete(1500), FRETE)


class TestTotal(unittest.TestCase):
    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(21000, 1)]), 21000)

    def test_frete_calculado_depois_do_desconto(self):
        # 21000 - 10% = 18900, que não passa de 20000: paga frete
        self.assertEqual(total([(21000, 1)], "DESC10"), 18900 + FRETE)

    def test_com_desconto_continua_com_frete_gratis(self):
        # 50000 - 20% = 40000: frete grátis
        self.assertEqual(total([(25000, 2)], "DESC20"), 40000)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + FRETE)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(10000, 1)], "XPTO")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(10000, 0)])


if __name__ == "__main__":
    unittest.main()
