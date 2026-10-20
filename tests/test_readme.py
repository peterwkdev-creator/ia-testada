"""O README: cada link relativo e cada script citado num comando existem."""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"


class TestReadme(unittest.TestCase):

    def setUp(self):
        self.texto = README.read_text(encoding="utf-8")

    def test_links_relativos_existem(self):
        links = [a for a in re.findall(r"\]\(([^)#]+)\)", self.texto)
                 if not re.match(r"[a-z]+:", a)]
        self.assertGreaterEqual(len(links), 1)
        for alvo in links:
            with self.subTest(link=alvo):
                self.assertTrue((RAIZ / alvo).exists())

    def test_scripts_dos_comandos_existem(self):
        blocos = re.findall(r"```bash\n(.*?)```", self.texto, re.S)
        scripts = re.findall(r"python (?:-I )?(\S+\.py)", "".join(blocos))
        self.assertGreaterEqual(len(scripts), 1)
        for script in scripts:
            with self.subTest(script=script):
                self.assertTrue((RAIZ / script).is_file())

    def test_cada_pasta_do_indice_tem_readme(self):
        pastas = re.findall(r"\[`([^`]+)`\]\(\1/\)", self.texto)
        self.assertGreaterEqual(len(pastas), 1)
        for pasta in pastas:
            with self.subTest(pasta=pasta):
                self.assertTrue((RAIZ / pasta / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
