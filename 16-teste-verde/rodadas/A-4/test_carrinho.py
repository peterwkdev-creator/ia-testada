"""Testes de unidade de carrinho.py."""

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

    def test_tipos_nao_inteiros(self):
        for qtd in (1.0, 2.5, "2", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_carrinho_vazio(self):
        self.assertEqual(subtotal([]), 0)

    def test_um_item(self):
        self.assertEqual(subtotal([(1234, 3)]), 3702)

    def test_varios_itens(self):
        self.assertEqual(subtotal([(1000, 2), (550, 1), (199, 10)]), 4540)

    def test_brinde_preco_zero(self):
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
        for cupom in ("XYZ", "desc10", ""):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_mesmo_abaixo_do_minimo(self):
        with self.assertRaises(ValueError):
            desconto(0, "XYZ")

    def test_desc10_no_minimo(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc10_abaixo_do_minimo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)

    def test_desc20_no_minimo(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_arredondamento_meio_centavo_sobe(self):
        # R$ 100,05 com 10% = 1000,5 centavos
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredondamento_para_baixo(self):
        # 1000,4 centavos
        self.assertEqual(desconto(10004, "DESC10"), 1000)
        # 6000,4 centavos
        self.assertEqual(desconto(30002, "DESC20"), 6000)

    def test_arredondamento_para_cima(self):
        # 1000,6 centavos
        self.assertEqual(desconto(10006, "DESC10"), 1001)
        # 6000,6 centavos
        self.assertEqual(desconto(30003, "DESC20"), 6001)


class TestFrete(unittest.TestCase):
    def test_valor_zero_paga_frete(self):
        self.assertEqual(frete(0), 1500)

    def test_exatamente_200_reais_paga_frete(self):
        self.assertEqual(frete(20000), 1500)

    def test_acima_de_200_reais_frete_gratis(self):
        self.assertEqual(frete(20001), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_so_frete(self):
        self.assertEqual(total([]), 1500)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 11500)

    def test_sem_cupom_exatamente_200_reais(self):
        self.assertEqual(total([(20000, 1)]), 21500)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 11499)

    def test_cupom_com_frete_gratis(self):
        # 30000 - 6000 = 24000, acima de 200 reais
        self.assertEqual(total([(10000, 3)], "DESC20"), 24000)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # 22000 passaria do limite, mas com 10% vira 19800 e paga frete
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + 1500)

    def test_desconto_deixa_exatamente_200_reais(self):
        # 22222 - 2222 = 20000, que ainda paga frete
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
