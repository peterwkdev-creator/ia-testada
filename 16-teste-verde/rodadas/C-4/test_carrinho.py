import unittest

from carrinho import desconto, frete, subtotal, total, validar_quantidade


class TestValidarQuantidade(unittest.TestCase):
    def test_limites_validos(self):
        for qtd in (1, 50, 99):
            with self.subTest(qtd=qtd):
                self.assertEqual(validar_quantidade(qtd), qtd)

    def test_fora_do_intervalo(self):
        for qtd in (0, -1, 100):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_bool_nao_vale(self):
        for qtd in (True, False):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_tipos_nao_inteiros(self):
        for qtd in (1.0, 2.5, "1", None):
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
        for qtd in (0, 100, True, 1.5):
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
            desconto(0, "XYZ")

    def test_desc10_minimo_inclusivo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc20_minimo_inclusivo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo_nao_aplica_desc10(self):
        self.assertEqual(desconto(15000, "DESC20"), 0)

    def test_arredondamento(self):
        casos = [
            (10004, "DESC10", 1000),  # 1000,4 desce
            (10005, "DESC10", 1001),  # 1000,5 sobe
            (10006, "DESC10", 1001),  # 1000,6 sobe
            (30002, "DESC20", 6000),  # 6000,4 desce
            (30003, "DESC20", 6001),  # 6000,6 sobe
        ]
        for valor, cupom, esperado in casos:
            with self.subTest(valor=valor, cupom=cupom):
                self.assertEqual(desconto(valor, cupom), esperado)


class TestFrete(unittest.TestCase):
    def test_cobra_frete_ate_o_limite(self):
        for valor in (0, 10000, 20000):
            with self.subTest(valor=valor):
                self.assertEqual(frete(valor), 1500)

    def test_frete_gratis_acima_do_limite(self):
        for valor in (20001, 50000):
            with self.subTest(valor=valor):
                self.assertEqual(frete(valor), 0)


class TestTotal(unittest.TestCase):
    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 11500)

    def test_sem_cupom_no_limite_do_frete(self):
        self.assertEqual(total([(20000, 1)]), 21500)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_carrinho_vazio_paga_frete(self):
        self.assertEqual(total([]), 1500)

    def test_cupom_abaixo_do_minimo(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 11499)

    def test_cupom_com_frete_gratis(self):
        self.assertEqual(total([(10000, 3)], "DESC20"), 24000)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # subtotal 22000 teria frete grátis, mas com desconto cai para 19800
        self.assertEqual(total([(11000, 2)], "DESC10"), 21300)

    def test_desconto_leva_exatamente_ao_limite_do_frete(self):
        # 22222 - 2222 = 20000, que não passa do limite
        self.assertEqual(total([(22222, 1)], "DESC10"), 21500)

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
