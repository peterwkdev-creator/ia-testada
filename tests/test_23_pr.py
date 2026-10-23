"""Testes do 23-pr/medir_pr.py: a classificação dos arquivos citados, com um texto inventado."""
import importlib.util
import json
import pathlib
import unittest

PASTA = pathlib.Path(__file__).resolve().parent.parent / "23-pr"
_spec = importlib.util.spec_from_file_location("medir_pr", PASTA / "medir_pr.py")
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)

NOMES = {"README.md": 2, "gravar.py": 1, "medir.py": 1, "CHANGELOG.md": 1}
TEXTO = """## Resumo
- `30-motion/gravar.py`: gravador quadro a quadro.
- medir.py novo no 19.
- 31-agent-teams entra com o teste.
- README atualizado; veja o README.md da pasta.
"""


class Classificar(unittest.TestCase):
    def c(self, caminho):
        return medir.classificar(caminho, TEXTO, NOMES)

    def test_caminho_inteiro(self):
        self.assertEqual(self.c("30-motion/gravar.py"), "caminho")

    def test_nome_unico(self):
        self.assertEqual(self.c("19-dicionario/medir.py"), "nome")

    def test_nome_repetido_e_ambiguo(self):
        self.assertEqual(self.c("30-motion/README.md"), "ambiguo")

    def test_so_a_pasta(self):
        self.assertEqual(self.c("31-agent-teams/medir_time.py"), "pasta")

    def test_fora(self):
        self.assertEqual(self.c("CHANGELOG.md"), "fora")

    def test_arquivo_da_raiz_pelo_nome(self):
        self.assertEqual(self.c("README.md"), "caminho")

    def test_pedaco_de_outro_caminho_nao_conta(self):
        self.assertEqual(medir.classificar("README.md", "veja 30-motion/README.md", NOMES), "fora")
        self.assertFalse(medir.aparece("medir.py", "o medir.pyc velho"))


class Comando(unittest.TestCase):
    def test_sem_claude_md_global_e_so_leitura_e_git(self):
        cmd = medir.comando("claude")
        self.assertEqual(cmd[:3], ["claude", "-p", medir.FRASE])
        excl = json.loads(cmd[cmd.index("--settings") + 1])["claudeMdExcludes"]
        self.assertTrue(excl[0].endswith(".claude/CLAUDE.md"))
        self.assertEqual(cmd[cmd.index("--tools") + 1], "Bash,Read,Grep,Glob")
        self.assertEqual(cmd[cmd.index("--allowedTools") + 1], "Bash(git *),Read,Grep,Glob")
        self.assertIn("--no-session-persistence", cmd)


if __name__ == "__main__":
    unittest.main()
