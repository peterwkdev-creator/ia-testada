"""O 30: o widget é o do chat, a moldura não o muda, e cada número
inventado está na linha dita e fora do prompt. Não grava vídeo (o gravar.py
pede o Playwright e o Chrome)."""
import csv
import hashlib
import re
import unittest
from pathlib import Path

PASTA = Path(__file__).resolve().parents[1] / "30-motion"
SHA_WIDGET = "23ac8faae514f10451451c2b030cfb1a5dfbc5a31879eb4c6375ede9b5b23cfa"


def formas(valor):
    """O valor como aparece no texto (71,3%) ou na chamada num(71.3, ...)."""
    numero = valor.removesuffix("%").removesuffix(" s")
    return {valor, numero.replace(",", ".")}


class TestMotion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.widget = (PASTA / "widget.html").read_bytes()
        cls.linhas = cls.widget.decode("utf-8").splitlines()
        cls.prompt = (PASTA / "prompt.txt").read_text(encoding="utf-8")
        with open(PASTA / "inventados.tsv", encoding="utf-8", newline="") as f:
            cls.inventados = list(csv.DictReader(f, delimiter="\t"))

    def test_widget_e_o_do_chat(self):
        self.assertEqual(hashlib.sha256(self.widget).hexdigest(), SHA_WIDGET)
        self.assertEqual(len(self.widget), 28708)
        self.assertEqual(len(self.linhas), 289)

    def test_moldura_tem_o_widget_inteiro(self):
        moldura = (PASTA / "index.html").read_bytes()
        self.assertIn(self.widget, moldura)
        self.assertIn(b"window.tl = tl", moldura)

    def test_dezoito_valores(self):
        valores = [i["valor"] for i in self.inventados]
        self.assertEqual(len(valores), 18)
        self.assertEqual(len(set(valores)), 18)

    def test_cada_valor_na_linha_dita(self):
        for i in self.inventados:
            for n in i["linhas do widget.html"].split(", "):
                with self.subTest(valor=i["valor"], linha=n):
                    linha = self.linhas[int(n) - 1]
                    self.assertTrue(any(f in linha for f in formas(i["valor"])))

    def test_nenhum_valor_no_prompt(self):
        for i in self.inventados:
            with self.subTest(valor=i["valor"]):
                for f in formas(i["valor"]):
                    self.assertNotIn(f, self.prompt)

    def test_prompt_tem_a_frase_e_so_dois_numeros(self):
        self.assertIn("Cada número com fonte e data", self.prompt)
        self.assertEqual(re.findall(r"\d+", self.prompt), ["1920", "1080", "30"])


if __name__ == "__main__":
    unittest.main()
