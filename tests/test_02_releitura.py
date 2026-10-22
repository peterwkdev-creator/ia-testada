"""Testes do 02-releitura/medir_sessao.py, com transcrições inventadas.

São as duas provas do `--provar` do medidor original: (1) plantado, uma
transcrição pequena com números conhecidos; (2) acervo, uma transcrição
maior, gerada aqui, em que as somas batem com uma conta independente.
Com a variável IA_TESTADA_TRANSCRICAO apontando para uma transcrição sua,
a prova 2 roda também nela (fica fora do CI).
"""
import collections
import importlib.util
import json
import os
import pathlib
import random
import re
import tempfile
import unittest

PASTA = pathlib.Path(__file__).resolve().parent.parent / "02-releitura"
_spec = importlib.util.spec_from_file_location("medir_sessao", PASTA / "medir_sessao.py")
ms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ms)

CHAVES = ("input_tokens", "cache_creation_input_tokens",
          "cache_read_input_tokens", "output_tokens")


def uso(**k):
    return {**{c: 0 for c in CHAVES}, **k}


def gravar(pasta, registros, extra=""):
    f = pathlib.Path(pasta) / "s.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in registros) + "\n" + extra, encoding="utf-8")
    return f


def conta_independente(caminho):
    """Primeira linha de cada message.id, somada sem passar pelo medidor."""
    soma, ids = collections.Counter(), set()
    for linha in caminho.open(encoding="utf-8"):
        try:
            e = json.loads(linha)
        except ValueError:
            continue
        m = e.get("message") or {}
        if e.get("type") == "assistant" and m.get("usage") and m.get("id") not in ids:
            ids.add(m.get("id"))
            soma.update({k: m["usage"].get(k) or 0 for k in CHAVES})
    return len(ids), soma


class Plantado(unittest.TestCase):
    """Prova 1: resposta repetida em duas linhas, reinício de cache,
    resultado de ferramenta conhecido e de id desconhecido, linha quebrada."""

    def setUp(self):
        reg = [
            {"type": "assistant", "message": {"id": "m1", "usage": uso(
                input_tokens=10, cache_creation_input_tokens=60000,
                cache_read_input_tokens=1000, output_tokens=2),
                "content": [{"type": "tool_use", "id": "t1", "name": "Read"}]}},
            # a mesma resposta em outra linha: conta uma vez
            {"type": "assistant", "message": {"id": "m1", "usage": uso(
                input_tokens=10, cache_creation_input_tokens=60000,
                cache_read_input_tokens=1000, output_tokens=2),
                "content": [{"type": "text", "text": "x"}]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t1", "content": "x" * 1000},
                {"type": "tool_result", "tool_use_id": "t9", "content": "abc"}]}},
            {"type": "assistant", "message": {"id": "m2", "usage": uso(
                cache_read_input_tokens=5000, output_tokens=4), "content": []}},
            {"type": "assistant", "message": {"id": "m3", "usage": uso(
                cache_creation_input_tokens=150000), "content": []}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            self.saida = ms.saida(gravar(tmp, reg, "linha quebrada\n"))

    def test_respostas_contadas_uma_vez(self):
        self.assertIn("respostas: 3\n", self.saida)

    def test_somas(self):
        for k, v in (("cache_creation_input_tokens", 210000), ("cache_read_input_tokens", 6000),
                     ("input_tokens", 10), ("output_tokens", 6)):
            with self.subTest(chave=k):
                self.assertIn(f"{k:30} {v:>14,}", self.saida)

    def test_reinicio_de_cache(self):
        self.assertIn("reinícios de cache (> 100 mil gravados): 1, somando 150,000", self.saida)

    def test_resultado_de_ferramenta(self):
        self.assertIn("Read                                             1x      1,000", self.saida)
        self.assertIn("?                                                1x          3", self.saida)

    def test_porcentagem_da_releitura(self):
        # 6.000 de 216.016 tokens
        self.assertRegex(self.saida, r"cache_read_input_tokens\s+6,000\s+2\.8%")


class Acervo(unittest.TestCase):
    """Prova 2: numa transcrição maior, as 4 somas e o número de respostas
    batem com a conta independente."""

    def conferir(self, caminho):
        n, soma = conta_independente(caminho)
        out = ms.saida(caminho)
        self.assertIn(f"respostas: {n}\n", out)
        for k, v in soma.items():
            with self.subTest(chave=k):
                self.assertIn(f"{k:30} {v:>14,}", out)

    def test_transcricao_sintetica(self):
        rnd = random.Random(2909)
        reg = []
        for i in range(300):
            u = uso(input_tokens=rnd.randint(0, 50),
                    cache_creation_input_tokens=rnd.choice([0, 500, 2000, 120000]),
                    cache_read_input_tokens=rnd.randint(20000, 160000),
                    output_tokens=rnd.randint(1, 900))
            for bloco in range(rnd.randint(1, 3)):  # um bloco por linha, o usage repetido
                reg.append({"type": "assistant", "message": {
                    "id": f"m{i}", "usage": u,
                    "content": [{"type": "tool_use", "id": f"t{i}-{bloco}", "name": "Bash"}]}})
            reg.append({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"t{i}-0", "content": "ok"}]}})
        with tempfile.TemporaryDirectory() as tmp:
            caminho = gravar(tmp, reg, "{quebrada\n")
            n, _ = conta_independente(caminho)
            self.assertEqual(n, 300)
            self.conferir(caminho)

    @unittest.skipUnless(os.environ.get("IA_TESTADA_TRANSCRICAO"),
                         "defina IA_TESTADA_TRANSCRICAO para rodar numa transcrição sua")
    def test_transcricao_sua(self):
        self.conferir(pathlib.Path(os.environ["IA_TESTADA_TRANSCRICAO"]))


class Uso(unittest.TestCase):
    def test_sem_argumento_mostra_o_uso(self):
        for argv in ([], ["a.jsonl", "b.jsonl"]):
            with self.subTest(argv=argv):
                with self.assertRaises(SystemExit) as fim:
                    ms.main(argv)
                self.assertIn("Uso: python -I medir_sessao.py", str(fim.exception.code))


class Medicao1810(unittest.TestCase):
    """A saída de 18/10/2026 que vai no repositório: sem o id da transcrição
    e com os números do post 2."""

    def setUp(self):
        self.texto = (PASTA / "medicao-1810.txt").read_text(encoding="utf-8")

    def test_sem_id_de_sessao(self):
        self.assertIsNone(re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}", self.texto))
        self.assertIn("transcript: <sessão>.jsonl", self.texto)

    def test_numeros_do_post(self):
        self.assertIn("respostas: 127", self.texto)
        self.assertRegex(self.texto, r"cache_read_input_tokens\s+13,257,338\s+98\.0%")
        self.assertRegex(self.texto, r"output_tokens\s+61,085\s+0\.5%")


if __name__ == "__main__":
    unittest.main()
