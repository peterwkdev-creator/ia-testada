"""Testes do 12-licenca/conferir_licencas.py: extração da licença com JSON de exemplo, sem rede."""
import importlib.util
import pathlib
import tempfile
import unittest

PASTA = pathlib.Path(__file__).resolve().parent.parent / "12-licenca"
_spec = importlib.util.spec_from_file_location("conferir_licencas", PASTA / "conferir_licencas.py")
conferir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(conferir)


class Extracao(unittest.TestCase):
    def test_codigo_com_licenca(self):
        self.assertEqual(conferir.licenca_codigo({"license": {"spdx_id": "MIT", "key": "mit"}}), "MIT")

    def test_codigo_sem_licenca(self):
        self.assertEqual(conferir.licenca_codigo({"license": None}), conferir.VAZIO)
        self.assertEqual(conferir.licenca_codigo({"license": {"spdx_id": None}}), conferir.VAZIO)
        self.assertEqual(conferir.licenca_codigo({}), conferir.VAZIO)

    def test_codigo_noassertion_e_mantido(self):
        self.assertEqual(conferir.licenca_codigo({"license": {"spdx_id": "NOASSERTION"}}), "NOASSERTION")

    def test_pesos_do_card(self):
        dados = {"cardData": {"license": "other", "license_name": "coqui-public-model-license"}}
        self.assertEqual(conferir.licenca_pesos(dados), ("other", "coqui-public-model-license"))

    def test_pesos_so_licenca(self):
        self.assertEqual(conferir.licenca_pesos({"cardData": {"license": "cc-by-nc-4.0"}}),
                         ("cc-by-nc-4.0", ""))

    def test_pesos_pela_tag(self):
        dados = {"cardData": None, "tags": ["tts", "license:mit", "region:us"]}
        self.assertEqual(conferir.licenca_pesos(dados), ("mit", ""))

    def test_pesos_sem_nada(self):
        self.assertEqual(conferir.licenca_pesos({}), (conferir.VAZIO, ""))

    def test_pesos_lista_no_card(self):
        self.assertEqual(conferir.licenca_pesos({"cardData": {"license": ["mit", "apache-2.0"]}}),
                         ("mit,apache-2.0", ""))


class Gravacao(unittest.TestCase):
    def test_tsv_utf8_com_cabecalho_e_data(self):
        linhas = [("F5-TTS", "SWivid/F5-TTS", "MIT", "SWivid/F5-TTS", "cc-by-nc-4.0", "",
                   "2026-10-26T12:00Z")]
        with tempfile.TemporaryDirectory() as tmp:
            destino = pathlib.Path(tmp) / "m.tsv"
            conferir.gravar(linhas, destino)
            texto = destino.read_text(encoding="utf-8")
        primeira, segunda = texto.splitlines()
        self.assertEqual(primeira.split("\t"), list(conferir.CABECALHO))
        self.assertEqual(segunda.split("\t")[2:5], ["MIT", "SWivid/F5-TTS", "cc-by-nc-4.0"])
        self.assertTrue(segunda.endswith("2026-10-26T12:00Z"))

    def test_seis_modelos(self):
        self.assertEqual(len(conferir.MODELOS), 6)


if __name__ == "__main__":
    unittest.main()
