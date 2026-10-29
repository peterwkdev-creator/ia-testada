import unittest

import carrinho
from carrinho import desconto, frete, subtotal, total, validar_quantidade


class TestConstantes(unittest.TestCase):
    def test_valores_documentados(self):
        self.assertEqual(carrinho.FRETE, 1500)
        self.assertEqual(carrinho.FRETE_GRATIS_ACIMA, 20000)
        self.assertEqual(carrinho.QTD_MAXIMA, 99)
        self.assertEqual(carrinho.CUPONS["DESC10"], (10, 10000))
        self.assertEqual(carrinho.CUPONS["DESC20"], (20, 30000))


class TestValidarQuantidade(unittest.TestCase):
    def test_limites_validos_devolvem_a_propria_quantidade(self):
        for qtd in (1, 2, 50, 98, 99):
            with self.subTest(qtd=qtd):
                self.assertEqual(validar_quantidade(qtd), qtd)

    def test_fora_da_faixa(self):
        for qtd in (0, -1, 100, 1000):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_bool_nao_vale(self):
        for qtd in (True, False):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_tipos_nao_inteiros(self):
        for qtd in (1.0, 2.5, "3", None, [1]):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_um_item(self):
        self.assertEqual(subtotal([(1234, 1)]), 1234)

    def test_multiplica_preco_pela_quantidade_e_soma(self):
        self.assertEqual(subtotal([(1000, 3), (250, 2), (1, 99)]), 3000 + 500 + 99)

    def test_brinde_preco_zero(self):
        self.assertEqual(subtotal([(0, 5), (700, 1)]), 700)

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            subtotal([(1000, 1), (-1, 1)])

    def test_quantidade_invalida_propaga_erro(self):
        for qtd in (0, 100, True, 1.5):
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

    def test_desc10_no_minimo_inclusive(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc10_abaixo_do_minimo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)
        self.assertEqual(desconto(0, "DESC10"), 0)

    def test_desc10_acima_do_minimo(self):
        self.assertEqual(desconto(25000, "DESC10"), 2500)

    def test_desc20_no_minimo_inclusive(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_desc20_acima_do_minimo(self):
        self.assertEqual(desconto(50000, "DESC20"), 10000)

    def test_meio_centavo_sobe(self):
        # exemplo da docstring: R$ 100,05 com 10% dá R$ 10,01
        self.assertEqual(desconto(10005, "DESC10"), 1001)
        # 20% de 300,03 = 60,006 -> 60,01; 20% de 300,02 = 60,004 -> 60,00
        self.assertEqual(desconto(30003, "DESC20"), 6001)
        self.assertEqual(desconto(30002, "DESC20"), 6000)

    def test_abaixo_de_meio_centavo_desce(self):
        self.assertEqual(desconto(10004, "DESC10"), 1000)

    def test_acima_de_meio_centavo_sobe(self):
        self.assertEqual(desconto(10006, "DESC10"), 1001)
        self.assertEqual(desconto(10009, "DESC10"), 1001)


class TestFrete(unittest.TestCase):
    def test_valor_baixo_paga_frete(self):
        self.assertEqual(frete(0), 1500)
        self.assertEqual(frete(5000), 1500)

    def test_duzentos_reais_exatos_ainda_paga(self):
        self.assertEqual(frete(20000), 1500)

    def test_um_centavo_acima_e_gratis(self):
        self.assertEqual(frete(20001), 0)

    def test_valor_alto_e_gratis(self):
        self.assertEqual(frete(100000), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_so_frete(self):
        self.assertEqual(total([]), 1500)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + 1500)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(10000, 3)]), 30000)

    def test_exatamente_duzentos_reais_paga_frete(self):
        self.assertEqual(total([(10000, 2)]), 20000 + 1500)

    def test_com_cupom_e_frete(self):
        # 100,00 - 10,00 = 90,00 + 15,00
        self.assertEqual(total([(10000, 1)], "DESC10"), 10500)

    def test_com_cupom_e_frete_gratis(self):
        # 400,00 - 80,00 = 320,00, sem frete
        self.assertEqual(total([(20000, 2)], "DESC20"), 32000)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # 220,00 sem cupom tem frete grátis; com DESC10 cai para 198,00 e paga frete
        self.assertEqual(total([(22000, 1)]), 22000)
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + 1500)

    def test_desconto_que_deixa_exatamente_duzentos_paga_frete(self):
        # 222,22 - 22,22 = 200,00 exatos -> paga frete
        self.assertEqual(total([(22222, 1)], "DESC10"), 20000 + 1500)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + 1500)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(10000, 1)], "NAOEXISTE")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])

    def test_arredondamento_no_total(self):
        # 100,05 - 10,01 = 90,04 + 15,00
        self.assertEqual(total([(10005, 1)], "DESC10"), 9004 + 1500)


if __name__ == "__main__":
    unittest.main()
