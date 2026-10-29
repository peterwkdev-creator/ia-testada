import unittest

from carrinho import desconto, frete, subtotal, total, validar_quantidade


class TestValidarQuantidade(unittest.TestCase):
    def test_limites_validos(self):
        self.assertEqual(validar_quantidade(1), 1)
        self.assertEqual(validar_quantidade(50), 50)
        self.assertEqual(validar_quantidade(99), 99)

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

    def test_tipo_nao_inteiro(self):
        for qtd in (1.0, 2.5, "2", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1000, 2), (250, 3)]), 2750)

    def test_brinde_com_preco_zero(self):
        self.assertEqual(subtotal([(0, 1), (1234, 1)]), 1234)

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
        for cupom in ("DESC50", "desc10", ""):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(100, "INVALIDO")

    def test_desc10_minimo_inclusive(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc20_minimo_inclusive(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_meio_centavo_sobe(self):
        # R$ 100,05 com 10% = R$ 10,005 -> R$ 10,01
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredonda_para_o_mais_proximo(self):
        # 10% de 10004 = 1000,4 -> 1000
        self.assertEqual(desconto(10004, "DESC10"), 1000)
        # 10% de 10006 = 1000,6 -> 1001
        self.assertEqual(desconto(10006, "DESC10"), 1001)
        # 20% de 30002 = 6000,4 -> 6000; de 30003 = 6000,6 -> 6001
        self.assertEqual(desconto(30002, "DESC20"), 6000)
        self.assertEqual(desconto(30003, "DESC20"), 6001)


class TestFrete(unittest.TestCase):
    def test_abaixo_do_limite_paga_frete(self):
        self.assertEqual(frete(0), 1500)
        self.assertEqual(frete(10000), 1500)

    def test_exatamente_200_reais_paga_frete(self):
        self.assertEqual(frete(20000), 1500)

    def test_acima_de_200_reais_frete_gratis(self):
        self.assertEqual(frete(20001), 0)
        self.assertEqual(frete(100000), 0)


class TestTotal(unittest.TestCase):
    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 1)]), 6500)

    def test_exatamente_200_reais_paga_frete(self):
        self.assertEqual(total([(10000, 2)]), 21500)

    def test_acima_de_200_reais_sem_frete(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(5000, 1)], "DESC10"), 6500)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # 220,00 - 10% = 198,00, que já não passa de 200,00: paga frete
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + 1500)

    def test_desconto_mantendo_frete_gratis(self):
        # 300,00 - 20% = 240,00: frete grátis
        self.assertEqual(total([(30000, 1)], "DESC20"), 24000)

    def test_varios_itens_com_cupom(self):
        # subtotal 250,00; 10% = 25,00; 225,00 sem frete
        self.assertEqual(total([(10000, 2), (2500, 2)], "DESC10"), 22500)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(5000, 1)], "NAOEXISTE")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
