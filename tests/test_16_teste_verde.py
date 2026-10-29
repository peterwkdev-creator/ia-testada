"""Testes do 16-teste-verde: os defeitos plantados importam e diferem do certo em uma
linha, a suíte de referência passa no certo e mata os 10, e o contar refaz as tabelas
gravadas a partir das suítes gravadas (sem rodar o Claude)."""
import importlib.util
import json
import pathlib
import unittest

PASTA = pathlib.Path(__file__).resolve().parent.parent / "16-teste-verde"
_spec = importlib.util.spec_from_file_location("medir_teste_verde", PASTA / "medir_teste_verde.py")
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)


class Defeitos(unittest.TestCase):
    def test_dez_defeitos_de_uma_linha(self):
        certo = medir.CARRINHO.read_text(encoding="utf-8").splitlines()
        lista = medir.defeitos()
        self.assertEqual(len(lista), 10)
        for d in lista:
            with self.subTest(defeito=d.name):
                mutante = d.read_text(encoding="utf-8").splitlines()
                self.assertEqual(len(mutante), len(certo))
                self.assertEqual(sum(a != b for a, b in zip(certo, mutante)), 1)

    def test_todo_defeito_importa(self):
        for d in medir.defeitos():
            with self.subTest(defeito=d.name):
                spec = importlib.util.spec_from_file_location(f"mutante_{d.stem}", d)
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                self.assertTrue(callable(modulo.total))

    def test_c_e_o_mesmo_codigo_sem_os_exemplos(self):
        certo_c = medir.PROJETO_C / "carrinho.py"
        self.assertEqual(medir.sem_docstrings(certo_c), medir.sem_docstrings(medir.CARRINHO))
        self.assertNotEqual(certo_c.read_bytes(), medir.CARRINHO.read_bytes())
        texto_c = certo_c.read_text(encoding="utf-8")
        for exemplo in ("100,05", "200,00 exatos", "Preço 0", "12,34"):
            with self.subTest(exemplo=exemplo):
                self.assertIn(exemplo, medir.CARRINHO.read_text(encoding="utf-8"))
                self.assertNotIn(exemplo, texto_c)

    def test_defeitos_c_sao_os_mesmos(self):
        lista_c = medir.defeitos(medir.DEFEITOS_C)
        self.assertEqual([d.name for d in lista_c], [d.name for d in medir.defeitos()])
        for d in lista_c:
            with self.subTest(defeito=d.name):
                self.assertEqual(medir.sem_docstrings(d),
                                 medir.sem_docstrings(medir.DEFEITOS / d.name))
                # a conferência por AST enxerga a linha trocada
                self.assertNotEqual(medir.sem_docstrings(d), medir.sem_docstrings(medir.CARRINHO))

    def test_referencia_passa_no_certo(self):
        codigo, rodados, caidos = medir.rodar_suite(medir.REFERENCIA, medir.CARRINHO)
        self.assertEqual(codigo, 0)
        self.assertGreater(rodados, 0)
        self.assertEqual(caidos, 0)

    def test_referencia_mata_cada_defeito(self):
        for d in medir.defeitos():
            with self.subTest(defeito=d.name):
                codigo, rodados, caidos = medir.rodar_suite(medir.REFERENCIA, d)
                self.assertNotEqual(codigo, 0)
                self.assertGreater(rodados, 0)
                self.assertGreater(caidos, 0)


class Contar(unittest.TestCase):
    def test_refaz_as_tabelas_gravadas(self):
        medidas, detalhe = medir.tabelas()
        self.assertEqual(medidas, (PASTA / "medidas.tsv").read_text(encoding="utf-8"))
        self.assertEqual(detalhe, (PASTA / "defeitos.tsv").read_text(encoding="utf-8"))

    def test_cinco_rodadas_por_condicao(self):
        nomes = [p.name for p in medir.rodadas_gravadas()]
        self.assertEqual(nomes, [f"{c}-{n}" for c in "ABC" for n in range(1, 6)])


class Comando(unittest.TestCase):
    def test_frases_e_ferramentas(self):
        self.assertEqual(medir.FRASES["C"], medir.FRASES["A"])
        self.assertEqual(medir.PROJETOS["C"], medir.PROJETO_C)
        for condicao in "ABC":
            cmd = medir.comando("claude", condicao)
            self.assertEqual(cmd[:3], ["claude", "-p", medir.FRASES[condicao]])
            excl = json.loads(cmd[cmd.index("--settings") + 1])["claudeMdExcludes"]
            self.assertTrue(excl[0].endswith(".claude/CLAUDE.md"))
            self.assertEqual(cmd[cmd.index("--tools") + 1], "Bash,Read,Write,Edit,Glob,Grep")
            self.assertEqual(cmd[cmd.index("--allowedTools") + 1],
                             "Bash(python *),Read,Write,Edit,Glob,Grep")
            self.assertIn("--no-session-persistence", cmd)
        self.assertTrue(medir.FRASES["B"].startswith(medir.FRASES["A"] + " Antes de terminar"))


if __name__ == "__main__":
    unittest.main()
