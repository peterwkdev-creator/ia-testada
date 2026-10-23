"""Testes do 31-agent-teams/medir_time.py, com um --json inventado."""
import importlib.util
import pathlib
import tempfile
import unittest
from unittest import mock

PASTA = pathlib.Path(__file__).resolve().parent.parent / "31-agent-teams"
_spec = importlib.util.spec_from_file_location("medir_time", PASTA / "medir_time.py")
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)


def transcricao(arquivo, respostas, total, sessao=None):
    t = {"file": arquivo, "project": "p", "responses": respostas, "compactions": 0,
         "total": total, "top": {"kind": "output", "name": "responses", "cost": 0}}
    if sessao is not None:
        t["session"] = sessao
    return t


def solo():
    return {"folder": "solo", "version": "1.6.4", "responses": 4, "total": 100_000,
            "transcripts": [transcricao("s.jsonl", 4, 100_000)], "subagents": [], "sources": []}


def time():
    """Líder e três teammates que responderam, mais um vazio (fica fora da contagem)."""
    return {"folder": "time", "version": "1.6.4", "responses": 15, "total": 410_000,
            "transcripts": [transcricao("l.jsonl", 6, 150_000)],
            "subagents": [transcricao("agent-azeta-1a.jsonl", 3, 90_000, "l"),
                          transcricao("agent-aalfa-2b.jsonl", 2, 80_000, "l"),
                          transcricao("agent-abeta-3c.jsonl", 4, 90_000, "l"),
                          transcricao("agent-avazio-4d.jsonl", 0, 0, "l")],
            "sources": []}


ESPERADO = [
    ("versao_claude_context_cost", "1.6.4"),
    ("solo_sessoes", 1),
    ("solo_respostas", 4),
    ("solo_tokens", 100_000),
    ("time_sessoes_lider", 1),
    ("time_lider_respostas", 6),
    ("time_lider_tokens", 150_000),
    ("time_teammates", 3),
    ("time_teammates_respostas", 9),
    ("time_teammates_tokens", 260_000),
    ("teammate_alfa_respostas", 2),
    ("teammate_alfa_tokens", 80_000),
    ("teammate_beta_respostas", 4),
    ("teammate_beta_tokens", 90_000),
    ("teammate_zeta_respostas", 3),
    ("teammate_zeta_tokens", 90_000),
    ("time_respostas", 15),
    ("time_tokens", 410_000),
    ("contextos_no_time", 4),
    ("razao_time_solo", "4.1"),
]


class TestResumo(unittest.TestCase):

    def test_medidas_do_inventado(self):
        self.assertEqual(medir.resumo(solo(), time()), ESPERADO)

    def test_solo_com_subagente_para(self):
        s = solo()
        s["subagents"] = [transcricao("agent-a1.jsonl", 1, 10, "s")]
        with self.assertRaises(SystemExit):
            medir.resumo(s, time())

    def test_time_sem_teammate_para(self):
        t = time()
        t["subagents"] = [transcricao("agent-a4.jsonl", 0, 0, "l")]
        with self.assertRaises(SystemExit):
            medir.resumo(solo(), t)

    def test_teammate_fora_do_padrao_para(self):
        t = time()
        t["subagents"][0] = transcricao("agent-1.jsonl", 3, 90_000, "l")
        with self.assertRaises(SystemExit):
            medir.resumo(solo(), t)

    def test_versoes_diferentes_param(self):
        t = time()
        t["version"] = "1.6.3"
        with self.assertRaises(SystemExit):
            medir.resumo(solo(), t)

    def test_json_antigo_para(self):
        s = solo()
        del s["subagents"]
        with self.assertRaises(SystemExit):
            medir.resumo(s, time())

    def test_pasta_sem_tokens_para(self):
        s = solo()
        s["total"] = 0
        with self.assertRaises(SystemExit):
            medir.resumo(s, time())


class TestCaminho(unittest.TestCase):

    def test_prefixo_longo_so_no_windows(self):
        with mock.patch.object(medir.os, "name", "nt"):
            self.assertTrue(medir.longo("C:\\a").startswith("\\\\?\\"))
            self.assertEqual(medir.longo("\\\\?\\C:\\a"), "\\\\?\\C:\\a")
        with mock.patch.object(medir.os, "name", "posix"):
            self.assertFalse(medir.longo("/a").startswith("\\\\?\\"))


class TestMain(unittest.TestCase):

    def test_grava_a_tabela(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = pathlib.Path(tmp) / "medidas.tsv"
            with mock.patch.object(medir, "rodar", side_effect=[solo(), time()]), \
                    mock.patch("builtins.print"):
                medir.main(["a", "b"], destino=destino, quando="23/10/2026")
            linhas = destino.read_text(encoding="utf-8").splitlines()
        self.assertEqual(linhas[0], "medida\tvalor")
        self.assertIn("razao_time_solo\t4.1", linhas)
        self.assertTrue(linhas[-1].startswith("# medido em 23/10/2026"))

    def test_argumentos_errados_param(self):
        with self.assertRaises(SystemExit):
            medir.main(["so-uma"])


class TestArquivos(unittest.TestCase):

    def test_medidas_tsv_publicado(self):
        linhas = dict(l.split("\t") for l in
                      (PASTA / "medidas.tsv").read_text(encoding="utf-8").splitlines()
                      if "\t" in l)
        self.assertEqual(linhas["solo_tokens"], "141260")
        self.assertEqual(linhas["time_tokens"], "564642")
        self.assertEqual(linhas["razao_time_solo"], "4.0")
        tokens = int(linhas["time_lider_tokens"]) + int(linhas["time_teammates_tokens"])
        self.assertEqual(tokens, int(linhas["time_tokens"]))
        por_teammate = {n: int(linhas[f"teammate_{n}_tokens"])
                        for n in ("cpf", "temperatura", "palavras")}
        self.assertEqual(por_teammate, {"cpf": 127088, "temperatura": 93365, "palavras": 125961})
        self.assertEqual(sum(por_teammate.values()), int(linhas["time_teammates_tokens"]))
        respostas = sum(int(linhas[f"teammate_{n}_respostas"]) for n in por_teammate)
        self.assertEqual(respostas, int(linhas["time_teammates_respostas"]))

    def test_tarefa_e_configuracao_existem(self):
        self.assertTrue((PASTA / "TAREFA.md").is_file())
        self.assertIn("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS",
                      (PASTA / "settings-time.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
