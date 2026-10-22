"""Testes do 05-agente/capturar.py: só as partes puras.

A captura abre o Chrome e a rede; o CI não roda isso. Aqui ficam o recorte,
o tsv, o capturas.tsv guardado e a garantia de que o script carrega sem o
`websockets` instalado.
"""
import importlib.util
import pathlib
import sys
import unittest
from unittest import mock

PASTA = pathlib.Path(__file__).resolve().parent.parent / "05-agente"


def carregar():
    spec = importlib.util.spec_from_file_location("capturar", PASTA / "capturar.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cap = carregar()


class Carrega(unittest.TestCase):
    def test_carrega_sem_websockets(self):
        with mock.patch.dict(sys.modules, {"websockets": None}):
            self.assertTrue(callable(carregar().recorte_y))


class Recorte(unittest.TestCase):
    def test_faixa_300_px_acima_da_frase(self):
        self.assertEqual(cap.recorte_y(1000, 5000), 700)

    def test_nao_passa_do_comeco(self):
        self.assertEqual(cap.recorte_y(120, 5000), 0)

    def test_nao_passa_do_fim(self):
        self.assertEqual(cap.recorte_y(4900, 5000), 5000 - cap.ALT_RECORTE)


class Tsv(unittest.TestCase):
    LINHAS = [("a", "https://x", "frase a", "ok"), ("b", "https://y", "frase b", "não achada")]

    def test_cabecalho_e_linhas(self):
        texto = cap.texto_tsv(self.LINHAS, "2026-10-20 23:23 UTC")
        self.assertEqual(texto.splitlines(), [
            "nome\turl\tfrase\tresultado\tdata",
            "a\thttps://x\tfrase a\tok\t2026-10-20 23:23 UTC",
            "b\thttps://y\tfrase b\tnão achada\t2026-10-20 23:23 UTC"])

    def test_tudo_ok(self):
        self.assertFalse(cap.tudo_ok(self.LINHAS))
        self.assertTrue(cap.tudo_ok(self.LINHAS[:1]))


class CapturasGuardadas(unittest.TestCase):
    """O capturas.tsv de 20/10/2026 bate com a lista de páginas do script."""

    def test_uma_linha_ok_por_pagina(self):
        texto = (PASTA / "capturas" / "capturas.tsv").read_text(encoding="utf-8")
        linhas = texto.splitlines()
        self.assertEqual(linhas[0] + "\n", cap.CABECALHO)
        guardadas = [tuple(l.split("\t")) for l in linhas[1:]]
        self.assertEqual([g[:3] for g in guardadas], [tuple(p) for p in cap.PAGINAS])
        self.assertTrue(all(g[3] == "ok" and g[4].startswith("2026-10-20") for g in guardadas))


if __name__ == "__main__":
    unittest.main()
