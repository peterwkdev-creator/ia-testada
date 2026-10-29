import unittest

from carrinho import (
    CUPONS,
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
    def test_limites_validos_devolvem_a_quantidade(self):
        for qtd in (1, 2, QTD_MAXIMA - 1, QTD_MAXIMA):
            with self.subTest(qtd=qtd):
                self.assertEqual(validar_quantidade(qtd), qtd)

    def test_fora_dos_limites_da_value_error(self):
        for qtd in (0, -1, QTD_MAXIMA + 1, 1000):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_bool_nao_vale_como_quantidade(self):
        for qtd in (True, False):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)

    def test_tipos_nao_inteiros_dao_value_error(self):
        for qtd in (1.0, 2.5, "3", None, [1]):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_lista_vazia_da_zero(self):
        self.assertEqual(subtotal([]), 0)

    def test_um_item(self):
        self.assertEqual(subtotal([(1990, 3)]), 5970)

    def test_varios_itens(self):
        self.assertEqual(subtotal([(1000, 2), (250, 4), (99, 1)]), 3099)

    def test_preco_zero_e_permitido(self):
        self.assertEqual(subtotal([(0, 5), (100, 1)]), 100)

    def test_preco_negativo_da_value_error(self):
        with self.assertRaises(ValueError):
            subtotal([(1000, 1), (-1, 1)])

    def test_quantidade_invalida_da_value_error(self):
        for qtd in (0, QTD_MAXIMA + 1, True, 1.5):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    subtotal([(1000, qtd)])

    def test_quantidade_maxima(self):
        self.assertEqual(subtotal([(100, QTD_MAXIMA)]), 100 * QTD_MAXIMA)


class TestDesconto(unittest.TestCase):
    def test_sem_cupom_da_zero(self):
        self.assertEqual(desconto(50000), 0)
        self.assertEqual(desconto(50000, None), 0)

    def test_cupom_desconhecido_da_value_error(self):
        for cupom in ("XYZ", "desc10", ""):
            with self.subTest(cupom=cupom):
                with self.assertRaises(ValueError):
                    desconto(50000, cupom)

    def test_cupom_desconhecido_da_erro_mesmo_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(0, "XYZ")

    def test_minimo_e_inclusivo(self):
        for cupom, (percentual, minimo) in CUPONS.items():
            with self.subTest(cupom=cupom):
                self.assertEqual(desconto(minimo, cupom), minimo * percentual // 100)
                self.assertEqual(desconto(minimo - 1, cupom), 0)

    def test_desc10(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)
        self.assertEqual(desconto(25000, "DESC10"), 2500)

    def test_desc20(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_arredonda_para_o_centavo_mais_proximo(self):
        # 10% de 10004 = 1000,4 -> 1000; 10% de 10006 = 1000,6 -> 1001
        self.assertEqual(desconto(10004, "DESC10"), 1000)
        self.assertEqual(desconto(10006, "DESC10"), 1001)
        # 20% de 30003 = 6000,6 -> 6001; 20% de 30001 = 6000,2 -> 6000
        self.assertEqual(desconto(30003, "DESC20"), 6001)
        self.assertEqual(desconto(30001, "DESC20"), 6000)

    def test_meio_centavo_sobe(self):
        # 10% de 10005 = 1000,5 -> 1001
        self.assertEqual(desconto(10005, "DESC10"), 1001)
        # 10% de 10015 = 1001,5 -> 1002 (não é arredondamento bancário)
        self.assertEqual(desconto(10015, "DESC10"), 1002)


class TestFrete(unittest.TestCase):
    def test_valor_baixo_paga_frete(self):
        self.assertEqual(frete(0), FRETE)
        self.assertEqual(frete(5000), FRETE)

    def test_exatamente_no_limite_ainda_paga_frete(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA), FRETE)

    def test_acima_do_limite_frete_gratis(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA + 1), 0)
        self.assertEqual(frete(100000), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_so_frete(self):
        self.assertEqual(total([]), FRETE)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(20001, 1)]), 20001)

    def test_sem_cupom_no_limite_paga_frete(self):
        self.assertEqual(total([(10000, 2)]), 20000 + FRETE)

    def test_com_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + FRETE)

    def test_com_cupom_e_frete(self):
        # 15000 - 1500 = 13500, + frete
        self.assertEqual(total([(15000, 1)], "DESC10"), 13500 + FRETE)

    def test_com_cupom_e_frete_gratis(self):
        # 40000 - 8000 = 32000, frete grátis
        self.assertEqual(total([(20000, 2)], "DESC20"), 32000)

    def test_frete_e_calculado_sobre_valor_com_desconto(self):
        # subtotal 22000 daria frete grátis, mas com desconto fica 19800
        self.assertEqual(total([(22000, 1)], "DESC10"), 19800 + FRETE)

    def test_desconto_arredondado_entra_no_total(self):
        # 10% de 10005 = 1000,5 -> 1001; 10005 - 1001 = 9004
        self.assertEqual(total([(10005, 1)], "DESC10"), 9004 + FRETE)

    def test_cupom_desconhecido_da_value_error(self):
        with self.assertRaises(ValueError):
            total([(5000, 1)], "XYZ")

    def test_item_invalido_propaga_value_error(self):
        with self.assertRaises(ValueError):
            total([(-100, 1)])
        with self.assertRaises(ValueError):
            total([(100, 0)])


if __name__ == "__main__":
    unittest.main()
