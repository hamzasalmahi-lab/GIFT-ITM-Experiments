import unittest
from pathlib import Path
import subprocess
import sys

class AuditThresholdTest(unittest.TestCase):
    def test_script_prints_expected_threshold(self):
        repo_root = Path(__file__).resolve().parents[1]
        script_path = repo_root / "audit_threshold.py"

        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            result.stdout.strip(),
            "The mathematically [PROVED] threshold is: Phi_th = L_bio*kappa/(2*lambda) + Phi_0",
        )


if __name__ == "__main__":
    unittest.main()