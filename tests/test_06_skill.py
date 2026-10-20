"""Testes do 06-skill/medir_skills.py, com SKILL.md e transcrição inventados."""
import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "06-skill" / "medir_skills.py"
_spec = importlib.util.spec_from_file_location("medir_skills", SCRIPT)
medir = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(medir)


def skill(pasta, nome, topo, corpo="Corpo da skill.\n", extras=None):
    d = pasta / nome
    d.mkdir(parents=True)
    texto = f"---\nname: {nome}\n{topo}---\n{corpo}"
    (d / "SKILL.md").write_bytes(texto.encode("utf-8"))
    for nome_extra, conteudo in (extras or {}).items():
        (d / nome_extra).write_bytes(conteudo)
    return len(texto)


class Descricao(unittest.TestCase):
    def test_sem_aspas(self):
        self.assertEqual(medir.descricao("name: x\ndescription: Faz uma coisa.\n"), 14)

    def test_aspas_duplas_nao_contam(self):
        self.assertEqual(medir.descricao('description: "Faz uma coisa."\n'), 14)

    def test_aspas_simples_nao_contam(self):
        self.assertEqual(medir.descricao("description: 'Faz uma coisa.'\n"), 14)

    def test_aspa_so_de_um_lado_conta(self):
        self.assertEqual(medir.descricao('description: "Faz uma coisa.\n'), 15)

    def test_acento_conta_um_caractere(self):
        self.assertEqual(medir.descricao("description: ação\n"), 4)

    def test_ausente(self):
        self.assertEqual(medir.descricao("name: x\n"), 0)


class Skills(unittest.TestCase):
    def test_pasta_inventada(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = pathlib.Path(tmp)
            n_b = skill(raiz / "synced" / "id-inventado", "beta", 'description: "Diz oi."\n',
                        extras={"ref.md": b"12345", "logo.png": b"\x00" * 10})
            n_a = skill(raiz, "alfa", "description: Faz.\ndisable-model-invocation: true\n")
            n_c = skill(raiz, "gama", "")
            self.assertEqual(list(medir.skills(raiz)), [
                ("alfa", 4, n_a, 0, "não"),
                ("beta", 7, n_b, 15, "sim"),
                ("gama", 0, n_c, 0, "sim"),
            ])


class Listagem(unittest.TestCase):
    def transcricao(self, registros):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = pathlib.Path(tmp.name) / "sessao.jsonl"
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in registros),
                     encoding="utf-8")
        return p

    def test_pega_a_inicial(self):
        p = self.transcricao([
            {"type": "user", "message": {"content": "oi"}},
            {"type": "attachment", "timestamp": "2026-01-01T10:00:00.000Z",
             "attachment": {"type": "skill_listing", "isInitial": False,
                            "skillCount": 1, "content": "x"}},
            {"type": "attachment", "timestamp": "2026-01-01T09:00:00.000Z",
             "attachment": {"type": "skill_listing", "isInitial": True,
                            "skillCount": 2, "content": "- alfa: Faz.\n- beta: Diz oi."}},
        ])
        self.assertEqual(medir.listagem(p), (2, 28, "2026-01-01T09:00:00.000Z"))

    def test_sem_listagem_inicial(self):
        p = self.transcricao([{"type": "attachment", "attachment": "texto"}])
        with self.assertRaises(SystemExit):
            medir.listagem(p)

    def test_tabela(self):
        texto = medir.tabela([("alfa", 4, 50, 0, "não")], 2, 28, "2026-01-01T09:00:00.000Z")
        self.assertEqual(texto,
                         "skill\tdescricao_chars\tskill_md_chars\toutros_bytes\tna_listagem\n"
                         "alfa\t4\t50\t0\tnão\n"
                         "\n"
                         "# listagem inicial da sessão (2026-01-01T09:00:00.000Z): 2 skills, 28 caracteres\n")


if __name__ == "__main__":
    unittest.main()
