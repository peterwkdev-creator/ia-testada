"""Testes de unidade de carrinho.py. Valores em centavos."""

import unittest

from carrinho import desconto, frete, subtotal, total, validar_quantidade


class TestValidarQuantidade(unittest.TestCase):
    def test_limites_validos(self):
        self.assertEqual(validar_quantidade(1), 1)
        self.assertEqual(validar_quantidade(50), 50)
        self.assertEqual(validar_quantidade(99), 99)

    def test_fora_dos_limites(self):
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
        for qtd in (1.0, "1", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1234, 2), (500, 3)]), 1234 * 2 + 500 * 3)

    def test_brinde_de_preco_zero(self):
        self.assertEqual(subtotal([(0, 5), (1000, 1)]), 1000)

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
        for cupom in ("XPTO", "desc10", ""):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(100, "XPTO")

    def test_desc10_minimo_inclusivo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc20_minimo_inclusivo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_arredonda_meio_centavo_para_cima(self):
        # R$ 100,05 com 10% = 1000,5 centavos -> 1001
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredonda_para_o_mais_proximo(self):
        self.assertEqual(desconto(10004, "DESC10"), 1000)  # 1000,4
        self.assertEqual(desconto(10006, "DESC10"), 1001)  # 1000,6
        self.assertEqual(desconto(30003, "DESC20"), 6001)  # 6000,6
        self.assertEqual(desconto(30002, "DESC20"), 6000)  # 6000,4


class TestFrete(unittest.TestCase):
    def test_cobra_frete_ate_o_limite_inclusive(self):
        self.assertEqual(frete(0), 1500)
        self.assertEqual(frete(19999), 1500)
        self.assertEqual(frete(20000), 1500)

    def test_frete_gratis_acima_do_limite(self):
        self.assertEqual(frete(20001), 0)
        self.assertEqual(frete(100000), 0)


class TestTotal(unittest.TestCase):
    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + 1500)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(22000, 1)]), 22000)

    def test_carrinho_vazio_paga_frete(self):
        self.assertEqual(total([]), 1500)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + 1500)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # 22000 passaria do limite, mas com 10% vira 19800 e paga frete
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + 1500)

    def test_valor_com_desconto_exatamente_no_limite_paga_frete(self):
        # 22222 - 2222 = 20000, que ainda paga frete
        self.assertEqual(total([(22222, 1)], "DESC10"), 20000 + 1500)

    def test_desconto_e_frete_gratis(self):
        # 30000 - 6000 = 24000, acima do limite
        self.assertEqual(total([(10000, 3)], "DESC20"), 24000)

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            total([(10000, 1)], "XPTO")

    def test_item_invalido(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
