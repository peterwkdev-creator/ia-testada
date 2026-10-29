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
        for qtd in (1, 2, QTD_MAXIMA):
            with self.subTest(qtd=qtd):
                self.assertEqual(validar_quantidade(qtd), qtd)

    def test_fora_do_intervalo(self):
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
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1000, 2), (550, 3)]), 3650)

    def test_brinde_preco_zero(self):
        self.assertEqual(subtotal([(0, 3), (1234, 1)]), 1234)

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

    def test_minimo_inclusivo(self):
        casos = [
            ("DESC10", 9999, 0),
            ("DESC10", 10000, 1000),
            ("DESC20", 29999, 0),
            ("DESC20", 30000, 6000),
        ]
        for cupom, valor, esperado in casos:
            with self.subTest(cupom=cupom, valor=valor):
                self.assertEqual(desconto(valor, cupom), esperado)

    def test_arredondamento(self):
        casos = [
            ("DESC10", 10004, 1000),  # 1000,4 desce
            ("DESC10", 10005, 1001),  # 1000,5 sobe (exemplo do docstring)
            ("DESC10", 10006, 1001),  # 1000,6 sobe
            ("DESC20", 30002, 6000),  # 6000,4 desce
            ("DESC20", 30003, 6001),  # 6000,6 sobe
        ]
        for cupom, valor, esperado in casos:
            with self.subTest(cupom=cupom, valor=valor):
                self.assertEqual(desconto(valor, cupom), esperado)


class TestFrete(unittest.TestCase):
    def test_cobra_frete_ate_o_limite(self):
        for valor in (0, 19999, 20000):
            with self.subTest(valor=valor):
                self.assertEqual(frete(valor), FRETE)

    def test_frete_gratis_acima_do_limite(self):
        for valor in (20001, 50000):
            with self.subTest(valor=valor):
                self.assertEqual(frete(valor), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_frete(self):
        self.assertEqual(total([]), FRETE)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(20000, 1)]), 20000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + FRETE)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # 220,00 sem desconto teria frete grátis; com 10% cai para 198,00
        self.assertEqual(total([(22000, 1)]), 22000)
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + FRETE)

    def test_valor_com_desconto_exatamente_no_limite_paga_frete(self):
        # 222,22 - 22,22 = 200,00 exatos
        self.assertEqual(total([(22222, 1)], "DESC10"), 20000 + FRETE)

    def test_desconto_e_frete_gratis(self):
        self.assertEqual(total([(15000, 2)], "DESC20"), 24000)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(10000, 1)], "XYZ")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(10000, 0)])


if __name__ == "__main__":
    unittest.main()
