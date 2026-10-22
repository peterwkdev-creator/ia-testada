"""O 19: o medir.py refaz os números do medidas.tsv, e os arquivos não levam
caminho nem id da nossa máquina ou conta."""
import importlib.util
import json
import pathlib
import re
import tempfile
import unittest

PASTA = pathlib.Path(__file__).resolve().parents[1] / "19-dicionario"
_spec = importlib.util.spec_from_file_location("medir_19", PASTA / "medir.py")
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)


class TestDicionario(unittest.TestCase):

    def test_medidas_batem_com_o_tsv(self):
        gravadas = medir.gravadas()
        for medida, valor in medir.medir().items():
            with self.subTest(medida=medida):
                self.assertEqual(str(valor), gravadas[medida])

    def test_numeros_do_post(self):
        self.assertEqual(medir.medir(), {
            "gancho_eventos": 3,
            "skill_descricao_caracteres": 244,
            "skill_corpo_caracteres": 4921,
            "mcp_chrome_ferramentas": 22,
        })
        gravadas = medir.gravadas()
        self.assertEqual(gravadas["razao_passo_subagente_sessao"], "0.50")
        self.assertEqual(gravadas["subagente_tokens"], "37900")

    def test_razao_igual_a_do_07(self):
        sete = medir.gravadas(PASTA.parent / "07-subagente" / "medidas.tsv")
        self.assertEqual(sete["razao_passo_subagente_sessao"],
                         medir.gravadas()["razao_passo_subagente_sessao"])

    def test_gancho_conta_so_eventos_do_teto(self):
        with tempfile.TemporaryDirectory() as d:
            arq = pathlib.Path(d) / "g.json"
            arq.write_text(json.dumps({"hooks": {
                "PreToolUse": [{"hooks": [{"command": "python teto-passos.py"}]}],
                "Stop": [{"hooks": [{"command": "python outro.py"}]}],
            }}), encoding="utf-8")
            self.assertEqual(medir.gancho_eventos(arq), 1)

    def test_ferramentas_unicas_e_do_chrome(self):
        nomes = (PASTA / "mcp-chrome.txt").read_text(encoding="utf-8").split()
        self.assertEqual(len(set(nomes)), len(nomes))
        self.assertTrue(all(n.startswith("mcp__claude-in-chrome__") for n in nomes))

    def test_sem_caminho_nem_id_da_conta(self):
        for arq in PASTA.rglob("*"):
            if arq.is_file() and arq.suffix in {".json", ".md", ".txt", ".tsv"}:
                texto = arq.read_text(encoding="utf-8")
                with self.subTest(arquivo=arq.name):
                    self.assertNotIn("Users/", texto)
                    self.assertNotIn("Users\\", texto)
                    # id da conta Meta: 15 ou mais dígitos que não sejam só zeros
                    ids = [n for n in re.findall(r"\d{15,}", texto) if set(n) != {"0"}]
                    self.assertEqual(ids, [])


if __name__ == "__main__":
    unittest.main()
