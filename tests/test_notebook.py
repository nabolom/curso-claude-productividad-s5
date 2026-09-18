import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "EJECUTA_S5_EN_LANGSMITH.ipynb"


class GuidedNotebookTests(unittest.TestCase):
    def setUp(self) -> None:
        with NOTEBOOK.open(encoding="utf-8") as file:
            self.notebook = json.load(file)
        self.source = "\n".join(
            "".join(cell.get("source", [])) for cell in self.notebook["cells"]
        )

    def test_notebook_has_the_expected_simple_flow(self) -> None:
        self.assertEqual(self.notebook["nbformat"], 4)
        self.assertEqual(len(self.notebook["cells"]), 7)
        code_cells = [
            cell for cell in self.notebook["cells"] if cell["cell_type"] == "code"
        ]
        self.assertEqual(len(code_cells), 3)

    def test_every_code_cell_compiles_in_a_notebook_context(self) -> None:
        for index, cell in enumerate(self.notebook["cells"], start=1):
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            compile(
                source,
                f"cell-{index}",
                "exec",
                flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
            )

    def test_credentials_are_hidden_and_never_hardcoded(self) -> None:
        self.assertIn("getpass.getpass", self.source)
        self.assertIn('os.environ.pop("LANGSMITH_API_KEY", None)', self.source)
        self.assertNotRegex(self.source, r"lsv2_pt_[A-Za-z0-9_-]{20,}")
        self.assertNotRegex(self.source, r"OPENROUTER_API_KEY\s*=")

    def test_notebook_creates_the_expected_trace(self) -> None:
        self.assertIn('LANGSMITH_TRACING"] = "true"', self.source)
        self.assertIn("S5-HillClimbing-Mi-Traza", self.source)
        self.assertIn('ejecutar_demo(modo="replay", max_iteraciones=5)', self.source)
        self.assertIn("cliente.runs.get_url", self.source)
        self.assertIn("✅ TU TRAZA ESTÁ LISTA", self.source)

    def test_notebook_points_only_to_the_public_course_repository(self) -> None:
        urls = re.findall(r"https://github\.com/[^\s\"')]+", self.source)
        self.assertEqual(
            urls,
            ["https://github.com/nabolom/curso-claude-productividad-s5.git"],
        )


if __name__ == "__main__":
    unittest.main()
