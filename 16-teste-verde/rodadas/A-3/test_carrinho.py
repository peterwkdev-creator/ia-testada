import unittest

from carrinho import (
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
    def test_limites_validos(self):
        self.assertEqual(validar_quantidade(1), 1)
        self.assertEqual(validar_quantidade(50), 50)
        self.assertEqual(validar_quantidade(QTD_MAXIMA), QTD_MAXIMA)

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
        for qtd in (1.0, 2.5, "3", None):
            with self.subTest(qtd=qtd):
                with self.assertRaises(ValueError):
                    validar_quantidade(qtd)


class TestSubtotal(unittest.TestCase):
    def test_lista_vazia(self):
        self.assertEqual(subtotal([]), 0)

    def test_soma_preco_vezes_quantidade(self):
        self.assertEqual(subtotal([(1234, 2), (500, 1), (99, 3)]), 1234 * 2 + 500 + 99 * 3)

    def test_brinde_com_preco_zero(self):
        self.assertEqual(subtotal([(0, 5), (1000, 1)]), 1000)

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
        with self.assertRaises(ValueError):
            desconto(50000, "DESC99")

    def test_cupom_desconhecido_abaixo_de_qualquer_minimo(self):
        with self.assertRaises(ValueError):
            desconto(100, "NAOEXISTE")

    def test_cupom_e_sensivel_a_maiusculas(self):
        with self.assertRaises(ValueError):
            desconto(50000, "desc10")

    def test_desc10_no_minimo_exato(self):
        self.assertEqual(desconto(10000, "DESC10"), 1000)

    def test_desc10_abaixo_do_minimo(self):
        self.assertEqual(desconto(9999, "DESC10"), 0)

    def test_desc20_no_minimo_exato(self):
        self.assertEqual(desconto(30000, "DESC20"), 6000)

    def test_desc20_abaixo_do_minimo(self):
        self.assertEqual(desconto(29999, "DESC20"), 0)

    def test_meio_centavo_arredonda_para_cima(self):
        # R$ 100,05 com 10% = 1000,5 centavos -> 1001
        self.assertEqual(desconto(10005, "DESC10"), 1001)

    def test_arredonda_para_baixo_abaixo_de_meio(self):
        # 10004 * 10% = 1000,4 -> 1000
        self.assertEqual(desconto(10004, "DESC10"), 1000)

    def test_arredonda_para_cima_acima_de_meio(self):
        # 10006 * 10% = 1000,6 -> 1001
        self.assertEqual(desconto(10006, "DESC10"), 1001)

    def test_arredondamento_desc20(self):
        # 30003 * 20% = 6000,6 -> 6001; 30002 * 20% = 6000,4 -> 6000
        self.assertEqual(desconto(30003, "DESC20"), 6001)
        self.assertEqual(desconto(30002, "DESC20"), 6000)


class TestFrete(unittest.TestCase):
    def test_valor_zero_paga_frete(self):
        self.assertEqual(frete(0), FRETE)

    def test_exatamente_no_limite_paga_frete(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA), FRETE)

    def test_um_centavo_acima_do_limite_e_gratis(self):
        self.assertEqual(frete(FRETE_GRATIS_ACIMA + 1), 0)

    def test_valores_concretos(self):
        self.assertEqual(FRETE, 1500)
        self.assertEqual(frete(20000), 1500)
        self.assertEqual(frete(20001), 0)


class TestTotal(unittest.TestCase):
    def test_carrinho_vazio_paga_so_frete(self):
        self.assertEqual(total([]), FRETE)

    def test_sem_cupom_com_frete(self):
        self.assertEqual(total([(5000, 2)]), 10000 + FRETE)

    def test_sem_cupom_frete_gratis(self):
        self.assertEqual(total([(10000, 2), (1, 1)]), 20001)

    def test_exatamente_200_paga_frete(self):
        self.assertEqual(total([(10000, 2)]), 20000 + FRETE)

    def test_cupom_abaixo_do_minimo_nao_desconta(self):
        self.assertEqual(total([(9999, 1)], "DESC10"), 9999 + FRETE)

    def test_cupom_aplicado_com_frete(self):
        # 10000 - 1000 = 9000, + frete
        self.assertEqual(total([(10000, 1)], "DESC10"), 9000 + FRETE)

    def test_frete_calculado_sobre_valor_com_desconto(self):
        # subtotal 21000 teria frete grátis, mas com DESC10 cai para 18900
        self.assertEqual(total([(21000, 1)]), 21000)
        self.assertEqual(total([(21000, 1)], "DESC10"), 18900 + FRETE)

    def test_desconto_no_limite_do_frete_ainda_paga(self):
        # 22222 com DESC10: desconto 2222 -> 20000 exatos, que ainda pagam frete
        self.assertEqual(total([(22222, 1)], "DESC10"), 20000 + FRETE)

    def test_desc20_com_frete_gratis(self):
        # 30000 - 6000 = 24000 > 20000 -> frete grátis
        self.assertEqual(total([(15000, 2)], "DESC20"), 24000)

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
