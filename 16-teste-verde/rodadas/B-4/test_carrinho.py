import unittest

import carrinho
from carrinho import desconto, frete, subtotal, total, validar_quantidade


class TestValidarQuantidade(unittest.TestCase):
    def test_limites_validos_sao_devolvidos(self):
        for qtd in (1, 2, 50, carrinho.QTD_MAXIMA):
            with self.subTest(qtd=qtd):
                self.assertEqual(validar_quantidade(qtd), qtd)

    def test_fora_da_faixa_da_value_error(self):
        for qtd in (0, -1, carrinho.QTD_MAXIMA + 1, 1000):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_bool_nao_vale(self):
        for qtd in (True, False):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_tipos_nao_inteiros_dao_value_error(self):
        for qtd in (1.0, 2.5, "2", None, [1]):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_lista_vazia_da_zero(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1234, 1)]), 1234)
        self.assertEqual(subtotal([(1000, 3), (250, 2), (1, 99)]), 3000 + 500 + 99)

    def test_brinde_com_preco_zero_vale(self):
        self.assertEqual(subtotal([(0, 5), (700, 1)]), 700)

    def test_preco_negativo_da_value_error(self):
        with self.assertRaises(ValueError):
            subtotal([(1000, 1), (-1, 1)])

    def test_quantidade_invalida_da_value_error(self):
        for qtd in (0, 100, True, 1.0):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    subtotal([(1000, qtd)])


class TestDesconto(unittest.TestCase):
    def test_sem_cupom_da_zero(self):
        self.assertEqual(desconto(50000), 0)
        self.assertEqual(desconto(50000, None), 0)

    def test_cupom_desconhecido_da_value_error(self):
        for cupom in ("XYZ", "desc10", "", "DESC10 "):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_da_erro_mesmo_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(0, "NADA")

    def test_desc10_no_minimo_exato_vale(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc10_abaixo_do_minimo_da_zero(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)

    def test_desc20_no_minimo_exato_vale(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo_da_zero(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_percentuais_diferentes_por_cupom(self):
        self.assertEqual(desconto(30000, "DESC10"), 3000)
        self.assertEqual(desconto(50000, "DESC20"), 10000)

    def test_meio_centavo_arredonda_para_cima(self):
        # R$ 100,05 com 10% = 1000,5 centavos -> 1001
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredonda_para_o_centavo_mais_proximo(self):
        self.assertEqual(desconto(10004, "DESC10"), 1000)  # 1000,4
        self.assertEqual(desconto(10006, "DESC10"), 1001)  # 1000,6
        self.assertEqual(desconto(30002, "DESC20"), 6000)  # 6000,4
        self.assertEqual(desconto(30003, "DESC20"), 6001)  # 6000,6


class TestFrete(unittest.TestCase):
    def test_ate_200_reais_paga_frete(self):
        for valor in (0, 1, 15000, 19999):
            with self.subTest(valor=valor):
                self.assertEqual(frete(valor), carrinho.FRETE)

    def test_200_reais_exatos_ainda_paga_frete(self):
        self.assertEqual(frete(20000), 1500)

    def test_acima_de_200_reais_frete_gratis(self):
        for valor in (20001, 50000):
            with self.subTest(valor=valor):
                self.assertEqual(frete(valor), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_so_o_frete(self):
        self.assertEqual(total([]), 1500)

    def test_sem_cupom_soma_subtotal_e_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + 1500)

    def test_limite_do_frete_gratis_sem_cupom(self):
        self.assertEqual(total([(20000, 1)]), 21500)
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + 1500)

    def test_cupom_aplicado(self):
        # 10000 - 1000 = 9000, + frete
        self.assertEqual(total([(10000, 1)], "DESC10"), 10500)
        # 50000 - 10000 = 40000, frete grátis
        self.assertEqual(total([(25000, 2)], "DESC20"), 40000)

    def test_frete_e_calculado_sobre_valor_com_desconto(self):
        # subtotal 21000 teria frete grátis, mas com desconto cai para 18900
        self.assertEqual(total([(21000, 1)], "DESC10"), 18900 + 1500)

    def test_valor_com_desconto_exatamente_200_paga_frete(self):
        # 22222 - 2222 = 20000 exatos -> ainda paga frete
        self.assertEqual(total([(22222, 1)], "DESC10"), 20000 + 1500)

    def test_cupom_desconhecido_da_value_error(self):
        with self.assertRaises(ValueError):
            total([(10000, 1)], "INVALIDO")

    def test_item_invalido_da_value_error(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
