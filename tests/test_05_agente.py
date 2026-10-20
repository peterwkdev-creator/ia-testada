"""Testes do 05-agente/conferir_fontes.py, com páginas inventadas (sem rede)."""
import contextlib
import http.client
import importlib.util
import io
import pathlib
import tempfile
import unittest
from unittest import mock

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "05-agente" / "conferir_fontes.py"
_spec = importlib.util.spec_from_file_location("conferir_fontes", SCRIPT)
conf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(conf)

FRASE = "usage counts against each person's own plan limits rather than yours"


class Texto(unittest.TestCase):
    def test_tira_tags_e_junta_espacos(self):
        self.assertEqual(conf.texto("<p>Artifacts <b>start</b>\n  private</p>"),
                         "Artifacts start private")

    def test_tira_script_e_style(self):
        self.assertEqual(conf.texto("<script>var a='x'</script>oi<style>p{}</style>"), "oi")

    def test_desfaz_entidades(self):
        self.assertEqual(conf.texto("can&#39;t&nbsp;share"), "can't share")

    def test_aspa_tipografica_vira_reta(self):
        self.assertEqual(conf.texto("person’s"), "person's")


class Conferir(unittest.TestCase):
    def test_frase_presente(self):
        pagina = f"<html><body><p>Your {FRASE}.</p></body></html>"
        self.assertEqual(conf.conferir(pagina, [FRASE]), [(FRASE, True)])

    def test_frase_quebrada_por_tag_e_aspa_tipografica(self):
        pagina = ("<p>usage counts against each <em>person’s</em>\n"
                  "own plan limits rather than yours</p>")
        self.assertEqual(conf.conferir(pagina, [FRASE]), [(FRASE, True)])

    def test_frase_mudada_e_pega(self):
        # a prova plantada: a página trocou "yours" por "the owner's"
        pagina = "<p>usage counts against each person's own plan limits rather than the owner's</p>"
        self.assertEqual(conf.conferir(pagina, [FRASE]), [(FRASE, False)])

    def test_frase_so_no_script_nao_conta(self):
        pagina = f"<script>const t = \"{FRASE}\"</script><p>outra coisa</p>"
        self.assertEqual(conf.conferir(pagina, [FRASE]), [(FRASE, False)])

    def test_caixa_nao_importa(self):
        self.assertEqual(conf.conferir("<p>ARTIFACTS START PRIVATE TO YOU</p>",
                                       ["Artifacts start private to you"]),
                         [("Artifacts start private to you", True)])


class Fontes(unittest.TestCase):
    def test_cada_fonte_tem_url_oficial_e_frase(self):
        for nome, url, frases in conf.FONTES:
            with self.subTest(fonte=nome):
                self.assertRegex(url, r"^https://(support|code|platform)\.claude\.com/")
                self.assertGreaterEqual(len(frases), 1)

    def test_tabela_tem_data_e_cabecalho(self):
        t = conf.tabela([("a", "https://x", 200, "frase", "sim")], "2026-10-20 12:00")
        self.assertEqual(t.splitlines()[:3], ["# lido em 2026-10-20 12:00 (UTC)",
                                              "fonte\turl\thttp\tfrase\tpresente",
                                              "a\thttps://x\t200\tfrase\tsim"])


class Main(unittest.TestCase):
    """O main() inteiro, com o download trocado e o tsv numa pasta temporária."""

    FONTES = [("ok", "https://code.claude.com/a", [FRASE]),
              ("fora", "https://code.claude.com/b", [FRASE])]

    def rodar(self, baixar):
        with tempfile.TemporaryDirectory() as pasta, \
                mock.patch.object(conf, "AQUI", pathlib.Path(pasta)), \
                mock.patch.object(conf, "FONTES", self.FONTES), \
                mock.patch.object(conf, "baixar", baixar), \
                contextlib.redirect_stdout(io.StringIO()):
            codigo = conf.main()
            tsv = (pathlib.Path(pasta) / "conferencia.tsv").read_text("utf-8")
        return codigo, tsv.splitlines()[2:]

    def test_tudo_presente_sai_com_zero(self):
        codigo, linhas = self.rodar(lambda url: (200, f"<p>{FRASE}</p>"))
        self.assertEqual(codigo, 0)
        self.assertEqual([l.split("\t")[-1] for l in linhas], ["sim", "sim"])

    def test_erro_de_rede_sai_com_um(self):
        def baixar(url):
            if url.endswith("/b"):
                raise OSError("sem rede")
            return 200, f"<p>{FRASE}</p>"
        codigo, linhas = self.rodar(baixar)
        self.assertEqual(codigo, 1)
        self.assertEqual(linhas[0].split("\t")[2:], ["200", FRASE, "sim"])
        self.assertEqual(linhas[1].split("\t")[2:], ["erro: sem rede", FRASE, "não"])

    def test_leitura_incompleta_nao_derruba(self):
        # IncompleteRead não é OSError: antes saía com traceback e o tsv velho ficava
        def baixar(url):
            raise http.client.IncompleteRead(b"meia")
        codigo, linhas = self.rodar(baixar)
        self.assertEqual(codigo, 1)
        self.assertTrue(all("\terro: " in l and l.endswith("\tnão") for l in linhas))


if __name__ == "__main__":
    unittest.main()
