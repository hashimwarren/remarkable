#!/usr/bin/env python3
"""Behavioral tests for deterministic helpers and focused package checks."""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_DIR / "scripts"


def run_script(name: str, *arguments: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *arguments],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def write_executable(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def write_command(path: Path, body: str) -> Path:
    """Create a discoverable command stub on POSIX and Windows."""
    if os.name != "nt":
        write_executable(path, body)
        return path
    python_stub = path.with_name(path.name + "_stub.py")
    python_stub.parent.mkdir(parents=True, exist_ok=True)
    python_stub.write_text(body, encoding="utf-8")
    command = path.with_suffix(".cmd")
    command.write_text(f'@"{sys.executable}" "{python_stub}" %*\r\n', encoding="utf-8")
    return command


class ContextDiscoveryTests(unittest.TestCase):
    def test_prioritizes_context_and_excludes_generated_and_secret_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "PRODUCT.md").write_text("Product", encoding="utf-8")
            (root / "DESIGN.md").write_text("Design", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "STYLE.md").write_text("Style", encoding="utf-8")
            (root / "docs" / "customer-messaging.md").write_text("Message", encoding="utf-8")
            (root / "node_modules").mkdir()
            (root / "node_modules" / "BRAND.md").write_text("Ignore", encoding="utf-8")
            (root / ".env").write_text("TOKEN=secret", encoding="utf-8")
            (root / "marketing-secrets.md").write_text("Ignore", encoding="utf-8")

            result = run_script("discover_context.py", "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            paths = [item["path"] for item in payload["files"]]
            self.assertEqual(paths[:3], ["PRODUCT.md", "DESIGN.md", "docs/STYLE.md"])
            self.assertIn("docs/customer-messaging.md", paths)
            self.assertNotIn("node_modules/BRAND.md", paths)
            self.assertNotIn("marketing-secrets.md", paths)
            self.assertNotIn(".env", paths)

    def test_succeeds_without_style_or_impeccable_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("Project", encoding="utf-8")
            result = run_script("discover_context.py", "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual([item["path"] for item in payload["files"]], ["README.md"])


class DraftReservationTests(unittest.TestCase):
    def test_never_overwrites_an_existing_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            drafts = root / "drafts"
            drafts.mkdir()
            existing = drafts / "why-premises-matter.md"
            existing.write_text("Keep me", encoding="utf-8")

            result = run_script(
                "reserve_draft.py",
                "Why premises matter",
                "--root",
                str(root),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["relative_path"], "drafts/why-premises-matter-2.md")
            self.assertEqual(existing.read_text(encoding="utf-8"), "Keep me")
            self.assertTrue(Path(payload["path"]).exists())


class OutlineReservationTests(unittest.TestCase):
    def test_reserves_and_reuses_predictable_outline_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            drafts = root / "drafts"
            drafts.mkdir()
            article = drafts / "article.md"
            article.write_text("# Article\n", encoding="utf-8")

            first = run_script("reserve_outline.py", str(article), "--root", str(root))
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            self.assertEqual(first_payload["status"], "reserved")
            self.assertEqual(first_payload["relative_path"], "drafts/article.outline.md")

            outline = Path(first_payload["path"])
            outline.write_text("Keep this outline", encoding="utf-8")
            second = run_script("reserve_outline.py", str(article), "--root", str(root))
            self.assertEqual(second.returncode, 0, second.stderr)
            second_payload = json.loads(second.stdout)
            self.assertEqual(second_payload["status"], "existing")
            self.assertEqual(outline.read_text(encoding="utf-8"), "Keep this outline")

    def test_rejects_articles_outside_the_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            article = Path(outside) / "article.md"
            article.write_text("# Article\n", encoding="utf-8")
            result = run_script("reserve_outline.py", str(article), "--root", str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(article.with_suffix(".outline.md").exists())

    def test_rejects_existing_outline_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            drafts = root / "drafts"
            drafts.mkdir()
            article = drafts / "article.md"
            article.write_text("# Article\n", encoding="utf-8")
            target = Path(outside) / "outside.md"
            target.write_text("Keep me", encoding="utf-8")
            outline = drafts / "article.outline.md"
            try:
                outline.symlink_to(target)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"symlinks unavailable: {error}")

            result = run_script("reserve_outline.py", str(article), "--root", str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(outline.is_symlink())
            self.assertEqual(target.read_text(encoding="utf-8"), "Keep me")


class SloplessTests(unittest.TestCase):
    def test_preflight_blocks_when_slopless_and_npx_are_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = dict(os.environ)
            env["PATH"] = ""
            result = run_script(
                "run_slopless.py",
                "--preflight",
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["required_package"], "slopless@0.2.36")

    def test_preflight_acquires_pinned_slopless_through_npx(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bin_dir = root / "bin"
            npx = bin_dir / "npx"
            log = root / "npx.log"
            write_command(
                npx,
                f"""#!/usr/bin/env python3
import pathlib
import sys
pathlib.Path({str(log)!r}).write_text(" ".join(sys.argv[1:]))
print("slopless <file> --help JSON")
""",
            )
            env = dict(os.environ)
            env["PATH"] = os.pathsep.join([str(bin_dir), str(Path(sys.executable).parent)])
            result = run_script(
                "run_slopless.py",
                "--preflight",
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ready")
            self.assertEqual(payload["source"], "npx")
            self.assertEqual(payload["version"], "0.2.36")
            self.assertIn("--yes slopless@0.2.36 --help", log.read_text(encoding="utf-8"))

    def test_exact_installed_version_is_used_without_npx(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / "node_modules" / ".bin" / "slopless"
            log = root / "installed.log"
            write_command(
                installed,
                f"""#!/usr/bin/env python3
import pathlib
import sys
pathlib.Path({str(log)!r}).write_text(" ".join(sys.argv[1:]))
if "--version" in sys.argv:
    print("slopless 0.2.36")
else:
    print("slopless <file> --help JSON")
""",
            )
            env = dict(os.environ)
            env["PATH"] = str(Path(sys.executable).parent)
            result = run_script(
                "run_slopless.py",
                "--preflight",
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["source"], "installed")
            self.assertEqual(payload["version"], "0.2.36")
            self.assertEqual(log.read_text(encoding="utf-8"), "--help")

    def test_captures_findings_and_confirms_a_clean_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("In a world where things change.", encoding="utf-8")
            bin_dir = root / "bin"
            command = bin_dir / "npx"
            write_command(
                command,
                """#!/usr/bin/env python3
import json
import pathlib
import sys
if "--help" in sys.argv:
    print("slopless <file> --help JSON")
    raise SystemExit(0)
assert sys.argv[1:3] == ["--yes", "slopless@0.2.36"]
text = pathlib.Path(sys.argv[-1]).read_text()
if "In a world" in text:
    print(json.dumps([{"filePath": sys.argv[-1], "messages": [{"ruleId": "slopless/prohibited-phrases"}]}]))
    raise SystemExit(1)
print(json.dumps([]))
""",
            )
            env = dict(os.environ)
            env["PATH"] = os.pathsep.join([str(bin_dir), str(Path(sys.executable).parent)])

            first = run_script(
                "run_slopless.py",
                str(draft),
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            first_payload = json.loads(first.stdout)
            self.assertEqual(first_payload["status"], "findings")
            self.assertEqual(first_payload["finding_count"], 1)
            self.assertEqual(first_payload["rule_type_count"], 1)
            self.assertEqual(first_payload["rule_ids"], ["slopless/prohibited-phrases"])
            self.assertTrue(Path(first_payload["findings_path"]).is_file())

            draft.write_text("Specific conditions changed this year.", encoding="utf-8")
            second = run_script(
                "run_slopless.py",
                str(draft),
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            second_payload = json.loads(second.stdout)
            self.assertEqual(second_payload["status"], "clean")
            self.assertEqual(second_payload["finding_count"], 0)
            self.assertNotEqual(first_payload["findings_path"], second_payload["findings_path"])

    def test_pinned_npx_replaces_a_mismatched_installed_slopless(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / "node_modules" / ".bin" / "slopless"
            npx = root / "bin" / "npx"
            installed_log = root / "installed.log"
            npx_log = root / "npx.log"
            write_command(
                installed,
                f"""#!/usr/bin/env python3
import pathlib
import sys
pathlib.Path({str(installed_log)!r}).write_text("used")
if "--version" in sys.argv:
    print("slopless 0.2.35")
else:
    print("unverified")
""",
            )
            write_command(
                npx,
                f"""#!/usr/bin/env python3
import pathlib
import sys
pathlib.Path({str(npx_log)!r}).write_text(" ".join(sys.argv[1:]))
print("slopless <file> --help JSON")
""",
            )
            env = dict(os.environ)
            env["PATH"] = os.pathsep.join(
                [str(root / "bin"), str(Path(sys.executable).parent)]
            )
            result = run_script(
                "run_slopless.py",
                "--preflight",
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["source"], "npx")
            self.assertEqual(payload["package"], "slopless@0.2.36")
            self.assertTrue(installed_log.exists())
            self.assertIn(
                "--yes slopless@0.2.36 --help",
                npx_log.read_text(encoding="utf-8"),
            )

    def test_pinned_npx_replaces_prerelease_installed_versions(self) -> None:
        for reported_version in ("0.2.36-beta.1", "0.2.36rc1"):
            with self.subTest(reported_version=reported_version):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    installed = root / "node_modules" / ".bin" / "slopless"
                    npx = root / "bin" / "npx"
                    npx_log = root / "npx.log"
                    write_command(
                        installed,
                        f"""#!/usr/bin/env python3
import sys
if "--version" in sys.argv:
    print("slopless {reported_version}")
else:
    print("prerelease")
""",
                    )
                    write_command(
                        npx,
                        f"""#!/usr/bin/env python3
import pathlib
import sys
pathlib.Path({str(npx_log)!r}).write_text(" ".join(sys.argv[1:]))
print("slopless <file> --help JSON")
""",
                    )
                    env = dict(os.environ)
                    env["PATH"] = os.pathsep.join(
                        [str(root / "bin"), str(Path(sys.executable).parent)]
                    )
                    result = run_script(
                        "run_slopless.py",
                        "--preflight",
                        "--project-root",
                        str(root),
                        env=env,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    payload = json.loads(result.stdout)
                    self.assertEqual(payload["source"], "npx")
                    self.assertIn(
                        "--yes slopless@0.2.36 --help",
                        npx_log.read_text(encoding="utf-8"),
                    )


class RoughdraftTests(unittest.TestCase):
    def test_missing_roughdraft_keeps_the_draft_available(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("Draft", encoding="utf-8")
            env = dict(os.environ)
            env["PATH"] = ""
            result = run_script(
                "open_roughdraft.py",
                str(draft),
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "missing")
            self.assertEqual(Path(payload["draft"]), draft.resolve())
            self.assertEqual(draft.read_bytes(), b"Draft")

    def test_uses_documented_non_watching_mode_when_supported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("Draft", encoding="utf-8")
            log = root / "roughdraft.log"
            command = root / "node_modules" / ".bin" / "roughdraft"
            write_command(
                command,
                f"""#!/usr/bin/env python3
import json
import pathlib
import sys
pathlib.Path({str(log)!r}).write_text(json.dumps(sys.argv[1:]))
if "--help" in sys.argv:
    print("open <path> --no-watch --json")
    raise SystemExit(0)
print(json.dumps({{"opened": True}}))
""",
            )

            result = run_script(
                "open_roughdraft.py",
                str(draft),
                "--project-root",
                str(root),
                "--no-watch",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "opened")
            arguments = json.loads(log.read_text(encoding="utf-8"))
            self.assertEqual(arguments[:2], ["open", str(draft)])
            self.assertIn("--no-watch", arguments[2:])
            self.assertIn("--json", arguments[2:])

    def test_default_watched_review_reports_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("Draft", encoding="utf-8")
            log = root / "roughdraft-watch.log"
            command = root / "node_modules" / ".bin" / "roughdraft"
            write_command(
                command,
                f"""#!/usr/bin/env python3
import json
import pathlib
import sys
if "--help" in sys.argv:
    print("open <path> --no-watch --timeout --json")
    raise SystemExit(0)
pathlib.Path({str(log)!r}).write_text(" ".join(sys.argv[1:]))
print(json.dumps({{
    "events": [
        {{"type": "review.started"}},
        {{"type": "review.completed", "feedbackCount": 2}},
    ],
    "timedOut": False,
}}, indent=2))
""",
            )
            result = run_script(
                "open_roughdraft.py",
                str(draft),
                "--project-root",
                str(root),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "review_completed")
            self.assertTrue(payload["watching"])
            command_text = log.read_text(encoding="utf-8")
            self.assertNotIn("--no-watch", command_text)
            self.assertIn("--json", command_text)
            self.assertEqual(payload["review_event"]["type"], "review.completed")

    def test_does_not_complete_a_timed_out_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("Draft", encoding="utf-8")
            command = root / "node_modules" / ".bin" / "roughdraft"
            write_command(
                command,
                """#!/usr/bin/env python3
import json
import sys
if "--help" in sys.argv:
    print("open <path> --no-watch --timeout --json")
    raise SystemExit(0)
print(json.dumps({
    "events": [{"type": "review.completed"}],
    "timedOut": True,
}, indent=2))
raise SystemExit(1)
""",
            )
            result = run_script(
                "open_roughdraft.py",
                str(draft),
                "--project-root",
                str(root),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "review_ended")
            self.assertIsNone(payload["review_event"])

    def test_does_not_treat_an_abandoned_review_as_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("Draft", encoding="utf-8")
            command = root / "node_modules" / ".bin" / "roughdraft"
            write_command(
                command,
                """#!/usr/bin/env python3
import json
import sys
if "--help" in sys.argv:
    print("open <path> --no-watch --timeout --json")
    raise SystemExit(0)
print(json.dumps({"event": "review.abandoned"}))
""",
            )
            result = run_script(
                "open_roughdraft.py",
                str(draft),
                "--project-root",
                str(root),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "review_abandoned")


class PackagingTests(unittest.TestCase):
    def test_packaged_instruction_links_resolve(self) -> None:
        sources = [SKILL_DIR / "SKILL.md", *sorted((SKILL_DIR / "references").rglob("*.md"))]
        for source in sources:
            for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", source.read_text(encoding="utf-8")):
                link = urlsplit(target)
                if link.scheme or link.netloc or not link.path:
                    continue
                with self.subTest(source=source.relative_to(SKILL_DIR), target=target):
                    self.assertTrue((source.parent / unquote(link.path)).is_file())

    def test_agent_metadata_declares_explicit_invocation(self) -> None:
        # Lint the canonical block declaration, not general YAML or runtime behavior.
        # Alternate YAML serializations require updating this deliberately scoped check.
        metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
        policies = re.findall(r"(?m)^policy:[ \t]*(?:#.*)?\n((?:[ \t]+.*\n|\n)*)", metadata + "\n")
        self.assertEqual(len(policies), 1, "Expected one top-level policy block")
        flags = re.findall(
            r"(?m)^  allow_implicit_invocation:[ \t]*([^#\n]*?)[ \t]*(?:#.*)?$",
            policies[0],
        )
        self.assertEqual(flags, ["false"])


if __name__ == "__main__":
    unittest.main()
