#!/usr/bin/env python3
"""Focused tests for Remarkable's deterministic helpers and instruction contract."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


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


class PremiseCouncilInstructionTests(unittest.TestCase):
    def test_premise_council_has_five_scouts_and_a_single_agent_fallback(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        transformation = (SKILL_DIR / "references" / "premise-transformation.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("0.7-beta", skill)
        self.assertIn("five-scout premise council", skill)
        self.assertIn("spawn five independent", transformation)
        self.assertIn("Assign the ten appeals exactly once", transformation)
        self.assertIn("launch scouts in waves", transformation)
        self.assertIn("Limited concurrency changes only how many waves run", transformation)
        self.assertIn("Begin finalist selection only after all five territories", transformation)
        self.assertIn("fully single-context fallback only when subagents cannot be spawned", transformation)
        self.assertIn("The main agent is the editor-in-chief", transformation)


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
            self.assertGreaterEqual(payload["skipped_secret_like"], 2)

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


class ArticleMapTests(unittest.TestCase):
    def test_creates_a_premise_grounded_roughdraft_map(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "PREMISE.md").write_text(
                """# Premise

## Audience
Christian parents

## Desired Movement
Choose repeatable practices.

## Premise
Household rhythms form children's loves.

## Why Now
Calendars increasingly choose the family's defaults.
""",
                encoding="utf-8",
            )
            result = run_script("create_article_map.py", "Household liturgies", "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            draft = Path(payload["path"])
            text = draft.read_text(encoding="utf-8")
            self.assertIn("Household rhythms form children's loves.", text)
            self.assertIn("## Opening", text)
            self.assertIn("## Argument", text)
            self.assertIn("## Visible evidence", text)
            self.assertIn("## Ending", text)
            self.assertIn("## Call to action", text)
            self.assertEqual(text.count("{>>"), 5)

    def test_article_map_never_overwrites_an_existing_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "PREMISE.md").write_text("## Premise\nA premise.\n", encoding="utf-8")
            drafts = root / "drafts"
            drafts.mkdir()
            existing = drafts / "article.md"
            existing.write_text("Keep me", encoding="utf-8")
            result = run_script("create_article_map.py", "Article", "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["relative_path"], "drafts/article-2.md")
            self.assertEqual(existing.read_text(encoding="utf-8"), "Keep me")


class SloplessTests(unittest.TestCase):
    def test_missing_slopless_and_npx_blocks_before_drafting(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("Draft", encoding="utf-8")
            env = dict(os.environ)
            env["PATH"] = ""
            result = run_script(
                "run_slopless.py",
                str(draft),
                "--project-root",
                str(root),
                env=env,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["required_package"], "slopless@0.2.23")

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
            self.assertIn("--yes slopless@0.2.23 --help", log.read_text(encoding="utf-8"))

    def test_captures_findings_and_confirms_a_clean_rerun(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("In a world where things change.", encoding="utf-8")
            command = root / "node_modules" / ".bin" / "slopless"
            write_command(
                command,
                """#!/usr/bin/env python3
import json
import pathlib
import sys
if "--help" in sys.argv:
    print("slopless <file> --help JSON")
    raise SystemExit(0)
text = pathlib.Path(sys.argv[1]).read_text()
if "In a world" in text:
    print(json.dumps([{"filePath": sys.argv[1], "messages": [{"ruleId": "slopless/prohibited-phrases"}]}]))
    raise SystemExit(1)
print(json.dumps([]))
""",
            )

            first = run_script(
                "run_slopless.py",
                str(draft),
                "--project-root",
                str(root),
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
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            second_payload = json.loads(second.stdout)
            self.assertEqual(second_payload["status"], "clean")
            self.assertEqual(second_payload["finding_count"], 0)
            self.assertNotEqual(first_payload["findings_path"], second_payload["findings_path"])


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
            self.assertEqual(payload["install_command"], "npm i -g roughdraft")
            self.assertTrue(draft.is_file())

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
pathlib.Path({str(log)!r}).write_text(" ".join(sys.argv[1:]))
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
            self.assertIn("--no-watch", payload["command"])
            self.assertIn("--json", payload["command"])
            self.assertIn("open", log.read_text(encoding="utf-8"))

    def test_waits_for_done_reviewing_by_default(self) -> None:
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
print(json.dumps({{"event": "review.completed", "feedbackCount": 2}}))
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


class InstructionContractTests(unittest.TestCase):
    def test_core_acceptance_contract_is_present(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        premise = (SKILL_DIR / "references" / "premise.md").read_text(encoding="utf-8")
        article = (SKILL_DIR / "references" / "article.md").read_text(encoding="utf-8")
        interface = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("What do you want the reader to realize", skill)
        self.assertIn("exactly three", skill.casefold())
        self.assertIn("Which premise should govern the article: A, B, or C?", skill)
        self.assertIn("structured user-input control", skill)
        self.assertIn("Make these bolder", skill)
        self.assertIn("selection by letter, direction name", skill)
        self.assertIn("Treat this release as `0.7-beta`", skill)
        self.assertIn("Create or update `PREMISE.md`", skill)
        self.assertIn("Do not put an argument, proof plan, evidence list, headline", skill)
        self.assertIn("Appeal: [one of the ten appeals]", skill)
        self.assertIn("Fascination: [advantage or archetype", skill)
        self.assertIn("800–1,200", skill)
        self.assertIn("Slopless", skill)
        self.assertIn("run_slopless.py --preflight", skill)
        self.assertIn("Never silently produce an unlinted English article", skill)
        self.assertIn("It flagged [initial count] issues", skill)
        self.assertIn("ran Slopless [run count] times in total", skill)
        self.assertIn("leave inline comments, or suggest changes", skill)
        self.assertIn("click **Done Reviewing**", skill)
        self.assertIn("Do not use `--no-watch` for this handoff", skill)
        self.assertIn("Wait for the wrapper to report `review_completed`", skill)
        self.assertIn("create_article_map.py", skill)
        self.assertIn("say **“Guide me”**", skill)
        self.assertIn("say **“Draft it”**", skill)
        self.assertIn("Go wider", skill)
        self.assertIn("pairwise distinctness", skill)
        self.assertIn("A. Run Remarkable critique", skill)
        self.assertIn("STOP and wait for the user's choice", skill)
        self.assertIn("automatically resume here with your feedback", skill)
        self.assertIn("Roughdraft", skill)
        self.assertIn("strategically different", premise)
        self.assertIn("## [A, B, or C]. [Distinctive direction name]", premise)
        self.assertIn("Do not add `Reader realization`", premise)
        self.assertIn("**Premise — [selected appeal]**", premise)
        transformation = (SKILL_DIR / "references" / "premise-transformation.md").read_text(encoding="utf-8")
        self.assertIn("Privately generate 12–20", transformation)
        self.assertIn("Make a premise bolder", transformation)
        self.assertIn("Use the fascination trigger as the control", transformation)
        self.assertIn("Never invent", article)
        self.assertIn("selected premise", article)
        self.assertIn("allow_implicit_invocation: false", interface)


if __name__ == "__main__":
    unittest.main()
