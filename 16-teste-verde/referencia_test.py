"""Suíte de referência: passa no projeto/carrinho.py certo e falha em cada um dos 10 defeitos.

É a prova de que os defeitos plantados são matáveis. Nunca entra na pasta
da rodada do Claude. O medir_teste_verde.py a roda numa pasta temporária,
ao lado de uma cópia do carrinho.py (o certo ou um mutante)."""
import unittest

import carrinho as c


class Quantidade(unittest.TestCase):
    def test_limites_inclusivos(self):
        self.assertEqual(c.validar_quantidade(1), 1)
        self.assertEqual(c.validar_quantidade(99), 99)

    def test_fora_dos_limites(self):
        for ruim in (0, -1, 100, 2.0, True, "3"):
            with self.subTest(ruim=ruim), self.assertRaises(ValueError):
                c.validar_quantidade(ruim)


class Subtotal(unittest.TestCase):
    def test_soma(self):
        self.assertEqual(c.subtotal([(1250, 2), (99, 3)]), 2797)
        self.assertEqual(c.subtotal([]), 0)

    def test_brinde_vale(self):
        self.assertEqual(c.subtotal([(0, 2), (500, 1)]), 500)

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            c.subtotal([(-1, 1)])

    def test_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            c.subtotal([(500, 0)])


class Desconto(unittest.TestCase):
    def test_sem_cupom(self):
        self.assertEqual(c.desconto(50000), 0)

    def test_minimo_inclusivo(self):
        self.assertEqual(c.desconto(10000, "DESC10"), 1000)
        self.assertEqual(c.desconto(9999, "DESC10"), 0)
        self.assertEqual(c.desconto(30000, "DESC20"), 6000)
        self.assertEqual(c.desconto(29999, "DESC20"), 0)
        self.assertEqual(c.desconto(25000, "DESC20"), 0)

    def test_arredondamento(self):
        self.assertEqual(c.desconto(10005, "DESC10"), 1001)  # 1000,5 sobe
        self.assertEqual(c.desconto(10004, "DESC10"), 1000)  # 1000,4 desce
        self.assertEqual(c.desconto(10009, "DESC10"), 1001)  # 1000,9 sobe

    def test_cupom_desconhecido(self):
        with self.assertRaises(ValueError):
            c.desconto(50000, "DESC99")


class Frete(unittest.TestCase):
    def test_fronteira(self):
        self.assertEqual(c.frete(0), 1500)
        self.assertEqual(c.frete(20000), 1500)
        self.assertEqual(c.frete(20001), 0)


class Total(unittest.TestCase):
    def test_sem_cupom(self):
        self.assertEqual(c.total([(5000, 1)]), 6500)
        self.assertEqual(c.total([(10000, 3)]), 30000)

    def test_frete_depois_do_desconto(self):
        # 21.000 - 10% = 18.900: abaixo de 20.000, paga frete
        self.assertEqual(c.total([(21000, 1)], "DESC10"), 20400)


if __name__ == "__main__":
    unittest.main()
