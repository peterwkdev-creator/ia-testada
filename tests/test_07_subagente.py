"""Testes do 07-subagente/medir_subagentes.py, com um --json inventado."""
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "07-subagente" / "medir_subagentes.py"
_spec = importlib.util.spec_from_file_location("medir_subagentes", SCRIPT)
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)


def transcricao(arquivo, respostas, total, sessao=None):
    t = {"file": arquivo, "project": "p", "responses": respostas, "compactions": 0,
         "total": total, "top": {"kind": "output", "name": "responses", "cost": 0}}
    if sessao is not None:
        t["session"] = sessao
    return t


def inventado():
    """Duas sessões que responderam e uma vazia; três subagentes, dois na s1."""
    return {
        "folder": "p", "version": "1.6.3", "responses": 25, "total": 1_670_000,
        "transcripts": [transcricao("s1.jsonl", 10, 1_000_000),  # 100 mil por passo
                        transcricao("s2.jsonl", 4, 200_000),     # 50 mil
                        transcricao("s3.jsonl", 0, 0)],
        "subagents": [transcricao("agent-a1.jsonl", 5, 250_000, "s1"),  # 50 mil
                      transcricao("agent-a2.jsonl", 2, 60_000, "s1"),   # 30 mil
                      transcricao("agent-a3.jsonl", 4, 160_000, "s2")],  # 40 mil
        "sources": [],
    }


ESPERADO = [
    ("versao_claude_context_cost", "1.6.3"),
    ("respostas_projeto", 25),
    ("tokens_projeto", 1_670_000),
    ("sessoes", 3),
    ("respostas_sessoes", 14),
    ("tokens_sessoes", 1_200_000),
    ("subagentes", 3),
    ("sessoes_com_subagente", 2),
    ("respostas_subagentes", 11),
    ("tokens_subagentes", 470_000),
    ("subagentes_pct_do_projeto", "28.1"),
    ("sessoes_com_resposta", 2),
    ("subagentes_com_resposta", 3),
    ("sessoes_no_peso", 2),
    ("passo_sessao_mediana", 75_000),
    ("passo_subagente_mediana", 40_000),
    ("passo_subagente_min", 30_000),
    ("passo_subagente_max", 50_000),
    ("razao_passo_subagente_sessao", "0.53"),
    # s1: 310 mil / 1,31 mi; s2: 160 mil / 360 mil
    ("peso_subagentes_na_sessao_pct_min", "23.7"),
    ("peso_subagentes_na_sessao_pct_mediana", "34.1"),
    ("peso_subagentes_na_sessao_pct_max", "44.4"),
]


class Resumo(unittest.TestCase):
    def test_inventado(self):
        self.assertEqual(medir.resumo(inventado()), ESPERADO)

    def test_sessao_vazia_nao_entra_no_passo(self):
        self.assertEqual(medir.por_passo(inventado()["transcripts"]), [100_000, 50_000])

    def test_saida_sem_nome_de_arquivo(self):
        texto = medir.tabela(medir.resumo(inventado()), "21/10/2026")
        for nome in ("s1", "s2", "agent-a1", ".jsonl"):
            self.assertNotIn(nome, texto)

    def test_subagente_sem_a_sessao_fica_fora_do_peso(self):
        dados = inventado()
        dados["subagents"].append(transcricao("agent-a4.jsonl", 1, 90_000, "apagada"))
        self.assertEqual([round(p, 1) for p in medir.peso_na_sessao(dados)], [23.7, 44.4])

    def test_sem_peso_nenhum(self):
        dados = inventado()
        for s in dados["subagents"]:
            s["session"] = "apagada"
        with self.assertRaises(SystemExit):
            medir.resumo(dados)

    def test_json_antigo_sem_subagentes(self):
        dados = inventado()
        del dados["subagents"]
        with self.assertRaises(SystemExit):
            medir.resumo(dados)

    def test_pasta_sem_subagente(self):
        dados = inventado()
        dados["subagents"] = []
        with self.assertRaises(SystemExit):
            medir.resumo(dados)


class Tabela(unittest.TestCase):
    def test_formato(self):
        self.assertEqual(medir.tabela([("a", 1), ("b", "0.5")], "21/10/2026"),
                         "medida\tvalor\na\t1\nb\t0.5\n\n"
                         "# medido em 21/10/2026; passo = uma resposta; tokens = contexto relido\n")


class Rodar(unittest.TestCase):
    def test_sem_o_medidor(self):
        with mock.patch.object(medir.shutil, "which", return_value=None):
            with self.assertRaises(SystemExit):
                medir.rodar("pasta")

    def test_medidor_com_erro(self):
        falhou = subprocess.CompletedProcess([], 2, "", "pasta não existe")
        with mock.patch.object(medir.shutil, "which", return_value="ccc"), \
                mock.patch.object(medir.subprocess, "run", return_value=falhou):
            with self.assertRaises(SystemExit):
                medir.rodar("pasta")

    def test_le_o_json(self):
        ok = subprocess.CompletedProcess([], 0, json.dumps(inventado()), "")
        with mock.patch.object(medir.shutil, "which", return_value="ccc"), \
                mock.patch.object(medir.subprocess, "run", return_value=ok) as run:
            self.assertEqual(medir.rodar("pasta"), inventado())
        self.assertEqual(run.call_args.args[0], ["ccc", "--json", "pasta"])


class Main(unittest.TestCase):
    def test_grava_o_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = pathlib.Path(tmp) / "medidas.tsv"
            with mock.patch.object(medir, "rodar", return_value=inventado()), \
                    mock.patch("sys.stdout"):
                medir.main(["pasta"], destino=destino, quando="21/10/2026")
            self.assertEqual(destino.read_text(encoding="utf-8"),
                             medir.tabela(ESPERADO, "21/10/2026"))

    def test_sem_argumento(self):
        with self.assertRaises(SystemExit):
            medir.main([])


if __name__ == "__main__":
    unittest.main()
