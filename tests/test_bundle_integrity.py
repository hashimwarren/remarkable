#!/usr/bin/env python3
"""Release-bundle integrity tests for Remarkable."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
VERIFIER = SKILL_DIR / "scripts" / "verify_bundle.py"


class ReleaseBundleIntegrityTests(unittest.TestCase):
    def copy_bundle(self, destination: Path) -> Path:
        target = destination / "remarkable"
        shutil.copytree(
            SKILL_DIR,
            target,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        return target

    def verify(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(root / "scripts" / "verify_bundle.py"), "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_clean_copy_into_empty_directory_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_bundle(Path(directory))
            result = self.verify(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "verified")
            self.assertEqual(payload["release"], "1.2.2")
            self.assertGreaterEqual(payload["checked_files"], 27)

    def test_mixed_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_bundle(Path(directory))
            premise = root / "references" / "premise.md"
            premise.write_text(
                premise.read_text(encoding="utf-8") + "\nStale overlay\n",
                encoding="utf-8",
            )
            result = self.verify(root)
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "mismatch")
            self.assertIn(
                "references/premise.md",
                [failure["path"] for failure in payload["failures"]],
            )

    def test_critical_contracts_match_1_2_2(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        premise = (SKILL_DIR / "references" / "premise.md").read_text(encoding="utf-8")
        wayfinding = (SKILL_DIR / "references" / "wayfinding.md").read_text(encoding="utf-8")

        self.assertIn("Treat this release as `1.2.2`.", skill)
        self.assertIn(
            "Who’s this for? What should they see differently—and why does that matter now?",
            premise,
        )
        self.assertIn("○ Route → ○ Outline → ○ Proof → ○ Approval", wayfinding)
        self.assertNotIn("○ Map →", wayfinding)


if __name__ == "__main__":
    unittest.main()
