"""Testes do 25-rebase/medir_rebase.py: roda os quatro cenários com git de verdade."""
import importlib.util
import pathlib
import tempfile
import unittest

PASTA = pathlib.Path(__file__).resolve().parent.parent / "25-rebase"
_spec = importlib.util.spec_from_file_location("medir_rebase", PASTA / "medir_rebase.py")
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)


class Cenarios(unittest.TestCase):
    def test_quem_apaga_o_commit_do_colega(self):
        esperado = [("force", "aceito", "não"), ("force_with_lease", "barrado", "sim"),
                    ("fetch_e_force_with_lease", "aceito", "não"),
                    ("fetch_e_force_if_includes", "barrado", "sim")]
        self.assertEqual([(l[0], l[3], l[4]) for l in medir.medir()], esperado)

    def test_tabela_grava_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = pathlib.Path(tmp) / "m.tsv"
            medir.main([], destino=destino, quando="23/10/2026")
            texto = destino.read_text(encoding="utf-8")
        self.assertTrue(texto.startswith("cenario\topcoes\tfetch_antes\tpush\t"))
        self.assertIn("# medido em 23/10/2026 com git version", texto)


if __name__ == "__main__":
    unittest.main()
