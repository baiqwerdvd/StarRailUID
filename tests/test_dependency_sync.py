from pathlib import Path
import tempfile
import unittest

from scripts.check_dependency_sync import ROOT, check_dependency_sync


class DependencySyncTests(unittest.TestCase):
    def test_runtime_pins_match(self):
        self.assertEqual(check_dependency_sync(ROOT), [])

    def test_stale_pip_pin_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("pyproject.toml", "uv.lock", "pdm.lock", "poetry.lock", "requirements.txt"):
                (root / name).write_bytes((ROOT / name).read_bytes())
            path = root / "requirements.txt"
            path.write_text(
                path.read_text().replace("starrail-damage-cal==4.2.1", "starrail-damage-cal==0.0.0")
            )
            errors = check_dependency_sync(root)
            self.assertTrue(any("starrail-damage-cal: requirements.txt=0.0.0" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
