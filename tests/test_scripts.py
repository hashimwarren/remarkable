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
        self.assertIn("1.0.0", skill)
        self.assertIn("five-scout premise council", skill)
        scout_preamble = skill.split("Before delegation, tell the user:", 1)[1].split(
            "If subagents are unavailable", 1
        )[0]
        self.assertNotIn("appeal", scout_preamble.casefold())
        self.assertNotIn("fascination", scout_preamble.casefold())
        self.assertIn("different persuasive territory", scout_preamble)
        self.assertIn("run five independent", transformation)
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
            self.assertIn("inside the project root", result.stderr)

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
            self.assertIn("symbolic link", result.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "Keep me")


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

## Likely Objection
Small repeated practices cannot overcome the wider culture.

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
            self.assertIn("Small repeated practices cannot overcome the wider culture.", text)
            self.assertIn("[Add the confirmed response direction before review.]", text)
            self.assertIn("## Opening", text)
            self.assertIn("## Argument", text)
            self.assertIn("## Practical framework", text)
            self.assertIn("[Add the approved framework body here, or remove only this heading and marker when skipped.]", text)
            self.assertIn("## Comprehension or story visual", text)
            self.assertIn("## Proof needs", text)
            self.assertIn("[HEADER IMAGE PLACEHOLDER:", text)
            self.assertIn("[PROOF VISUAL PLACEHOLDER:", text)
            self.assertIn("[COMPREHENSION OR STORY VISUAL PLACEHOLDER:", text)
            self.assertIn("The article should make the reader want to understand", text)
            self.assertIn("The answer becomes clear", text)
            self.assertIn("How the article resolves it", text)
            self.assertNotIn("Framework's role", text)
            self.assertIn("otherwise state the premise directly", text)
            self.assertNotIn("consequential or surprising", text)
            self.assertNotIn("Approved Personal Authority", text)
            self.assertNotIn("open loop", text.casefold())
            self.assertIn("## Ending", text)
            self.assertIn("## Call to action", text)
            self.assertEqual(text.count("{>>"), 4)

    def test_carries_only_the_approved_personal_authority_story(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "PREMISE.md").write_text(
                """# Premise

## Audience
Startup founders

## Desired Movement
Direct AI as an editorial process before polishing prose.

## Premise
Great AI writing depends on editorial direction, not merely better prompting.

## Likely Objection
The model should infer the structure from a detailed recording.

## Why Now
More founders are using the same capable models with very different results.

## Personal Authority

Approach: Earned Discovery

**Approved story:**
I could get useful copy from the same kind of AI that produced an unusable article for a startup founder.
The difference was the editorial process I carried in my head.
""",
                encoding="utf-8",
            )
            result = run_script("create_article_map.py", "Editorial direction", "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            text = Path(json.loads(result.stdout)["path"]).read_text(encoding="utf-8")
            self.assertIn("Approved Personal Authority", text)
            self.assertIn("I could get useful copy from the same kind of AI", text)
            self.assertIn("The difference was the editorial process", text)
            self.assertNotIn("Approach: Earned Discovery", text)
            self.assertNotIn("open loop", text.casefold())

    def test_ignores_personal_authority_without_an_approved_story(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "PREMISE.md").write_text(
                """## Premise
A useful premise.

## Personal Authority
Approach: Earned Discovery

Unconfirmed notes that must not enter the map.
""",
                encoding="utf-8",
            )
            result = run_script("create_article_map.py", "Article", "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            text = Path(json.loads(result.stdout)["path"]).read_text(encoding="utf-8")
            self.assertNotIn("Approved Personal Authority", text)
            self.assertNotIn("Unconfirmed notes", text)

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
            self.assertNotEqual(payload["status"], "review_completed")


class InstructionContractTests(unittest.TestCase):
    def test_core_acceptance_contract_is_present(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        premise = (SKILL_DIR / "references" / "premise.md").read_text(encoding="utf-8")
        article = (SKILL_DIR / "references" / "article.md").read_text(encoding="utf-8")
        personal = (SKILL_DIR / "references" / "personal-authority.md").read_text(
            encoding="utf-8"
        )
        interface = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn("What do you want the reader to realize", skill)
        self.assertIn("exactly three", skill.casefold())
        self.assertIn("Which premise should govern the article: A, B, or C?", skill)
        self.assertIn("structured user-input control", skill)
        self.assertIn("Make these bolder", skill)
        self.assertIn("selection by letter, direction name", skill)
        self.assertIn("Treat this release as `1.0.0`", skill)
        self.assertIn("Create or update `PREMISE.md`", skill)
        self.assertIn("Do not put an argument, proof plan, evidence list, headline", skill)
        self.assertIn("## Likely Objection", skill)
        self.assertNotIn("Appeal: [one of the ten appeals]", skill)
        self.assertNotIn("Fascination: [advantage or archetype", skill)
        self.assertIn("Is there something you discovered, struggled through", skill)
        self.assertIn("Yes — I’ll tell you", skill)
        self.assertIn("references/personal-authority.md", skill)
        self.assertIn("references/objection-response.md", skill)
        self.assertIn("references/outline.md", skill)
        self.assertIn("Yes — I’ll answer", skill)
        self.assertIn("reserve_outline.py", skill)
        self.assertIn("Complete the map", skill)
        self.assertNotIn("**Draft it**", skill)
        self.assertIn("Draft this structure", skill)
        self.assertIn("If no outline exists, route to `outline`", skill)
        self.assertIn("never infer approval from file existence", skill)
        self.assertIn("Status: approved", skill)
        self.assertIn("reopen watched Roughdraft", skill)
        self.assertIn("resolved CriticMarkup questions", skill)
        self.assertIn("[EVIDENCE NEEDED: ...]", skill)
        self.assertIn("derive a fresh strongest intelligent likely objection", skill)
        self.assertNotIn("[When a personal story was approved", skill)
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
        self.assertIn("Roughdraft failure must never strand the article", skill)
        self.assertIn("continue that same review in chat", skill)
        self.assertIn("Never treat an unavailable or incomplete Roughdraft session as approval", skill)
        self.assertIn("create_article_map.py", skill)
        self.assertIn("**Open Roughdraft**", skill)
        self.assertIn("STOP and wait for the user's selection", skill)
        self.assertIn("stop the watched process", skill)
        self.assertIn("Go wider", skill)
        self.assertIn("pairwise distinctness", skill)
        self.assertIn("A. Run Remarkable critique", skill)
        self.assertIn("STOP and wait for the user's choice", skill)
        self.assertIn("automatically resume here with your feedback", skill)
        self.assertIn("Roughdraft", skill)
        self.assertIn("strategically different", premise)
        self.assertIn("## [A, B, or C]. [Distinctive direction name]", premise)
        self.assertIn("Do not add `Reader realization`", premise)
        self.assertIn("**Premise**", premise)
        self.assertIn("**Likely objection**", premise)
        self.assertNotIn("**Fascination —", premise)
        self.assertNotIn("**Risk**", premise)
        self.assertIn("Earned Discovery", personal)
        self.assertIn("Shared Struggle", personal)
        self.assertIn("Transformation", personal)
        self.assertIn("must never be a specific person—public or private—or a vulnerable group", personal)
        self.assertIn("If the writer skips Personal Authority, omit the entire section", personal)
        self.assertNotIn("**Recommended placement:**", personal)
        self.assertEqual(personal.count("```markdown"), 2)
        transformation = (SKILL_DIR / "references" / "premise-transformation.md").read_text(encoding="utf-8")
        self.assertIn("Privately generate 12–20", transformation)
        self.assertIn("Make a premise bolder", transformation)
        self.assertIn("Use the fascination trigger as the control", transformation)
        self.assertIn("Never invent", article)
        self.assertIn("selected premise", article)
        objection = (SKILL_DIR / "references" / "objection-response.md").read_text(
            encoding="utf-8"
        )
        prove = (SKILL_DIR / "references" / "prove.md").read_text(encoding="utf-8")
        outline = (SKILL_DIR / "references" / "outline.md").read_text(encoding="utf-8")
        critique = (SKILL_DIR / "references" / "critique.md").read_text(encoding="utf-8")
        narrative = (SKILL_DIR / "references" / "narrative-tension.md").read_text(
            encoding="utf-8"
        )
        wayfinding = (SKILL_DIR / "references" / "wayfinding.md").read_text(encoding="utf-8")
        visuals = (SKILL_DIR / "references" / "visual-placeholders.md").read_text(encoding="utf-8")
        frameworks = (SKILL_DIR / "references" / "framework-design.md").read_text(encoding="utf-8")
        self.assertIn("Store only the objection in `PREMISE.md`", objection)
        self.assertIn("A widened, intensified, combined", objection)
        self.assertIn("Objection pressure-testing is still premise formation", objection)
        self.assertIn("after the article map is resolved and before the working outline", prove)
        self.assertIn("## Claim-to-evidence plan", prove)
        self.assertIn("300–700", outline)
        self.assertIn("Blocking", outline)
        self.assertIn("AUTHOR INPUT NEEDED", outline)
        self.assertIn("generated header-image placeholder", outline)
        self.assertIn("Review revisions one by one", critique)
        self.assertIn("Apply recommended revisions", critique)
        self.assertIn("Leave the draft unchanged", critique)
        self.assertIn("patch the existing article", critique)
        self.assertIn("This version is ready for you to use", wayfinding)
        self.assertIn("Run another Remarkable critique", wayfinding)
        self.assertIn("● Premise", wayfinding)
        self.assertIn("○ Slopless", wayfinding)
        self.assertIn("○ Framework", wayfinding)
        self.assertIn("○ Map → ○ Proof → ○ Outline", wayfinding)
        self.assertIn("Slopless current", skill)
        self.assertIn("Mark Slopless complete", skill)
        self.assertIn("skipped with `–` for a non-English draft", skill)
        self.assertIn("dedicated visual subagent", visuals)
        self.assertIn("image-generation model", visuals)
        self.assertIn("public web", visuals)
        self.assertIn("one asset per turn", visuals)
        self.assertIn("never invent a path", visuals)
        self.assertIn("Attribution alone is not permission", visuals)
        self.assertIn("public-domain, Creative Commons", visuals)
        self.assertIn("Partial acceptance authorizes only", critique)
        self.assertIn("blanket approval does not authorize", critique)
        self.assertIn("make no rhetorical edits", critique)
        self.assertIn("Ambiguous reply", critique)
        self.assertIn("no further rhetorical revision is necessary", critique)
        self.assertIn("same choices as a short plain-text fallback", critique)
        self.assertIn("at most three buttons", wayfinding)
        self.assertIn("Low-fidelity outline concepts and placeholders", skill)
        self.assertNotIn("beta boundaries", skill.casefold())
        self.assertIn("references/framework-design.md", skill)
        self.assertIn("Develop the framework", skill)
        self.assertIn("Keep it as prose", skill)
        self.assertIn("mark framework skipped with `–`", skill)
        self.assertIn("Never write it to `PREMISE.md`", skill)
        self.assertIn("Whole / Parts / Whole", frameworks)
        self.assertIn("Formula", frameworks)
        self.assertIn("Progression", frameworks)
        self.assertIn("Categories", frameworks)
        self.assertIn("Decision Tree", frameworks)
        self.assertIn("Do not apply a Tier 2 technique", frameworks)
        self.assertIn("run a Tier 2 checkpoint in this release", frameworks)
        self.assertIn("Continue directly to the article map without mentioning frameworks", frameworks)
        self.assertIn("Never interpret enthusiasm, silence", frameworks)
        self.assertIn("Never write it to `PREMISE.md` or a separate framework artifact", frameworks)
        self.assertIn("converts ordinary bullets into an acronym", frameworks)
        self.assertIn("approved practical framework", outline)
        self.assertIn("where that answer becomes clear", outline)
        self.assertIn("Before the answer, every section must", outline)
        self.assertIn("After the answer, every section must", outline)
        self.assertIn("Do not default to a literal question", outline)
        self.assertIn("approved practical framework", visuals)
        self.assertIn("**Develop it:** explicitly approves", frameworks)
        self.assertIn("**Revise the logic:**", frameworks)
        self.assertIn("repeat this confirmation checkpoint", frameworks)
        self.assertIn("**Try another structure:**", frameworks)
        self.assertIn("genuinely different Tier 1 structure", frameworks)
        self.assertIn("same choices as a plain-text fallback", frameworks)
        self.assertIn("free-form request to **Keep it as prose**", frameworks)
        self.assertIn("Persist no framework", frameworks)
        self.assertIn("before creating the article map", frameworks)
        self.assertIn("hold it for insertion into the article map created next", frameworks)
        self.assertIn("Focused mode without an article map", frameworks)
        self.assertIn("**Create an article map** or **Keep it in chat**", frameworks)
        self.assertIn("body-only block", frameworks)
        self.assertNotIn("[FRAMEWORK VISUAL PLACEHOLDER:", frameworks)
        self.assertIn("remove only the `## Practical framework` heading and its marker", skill)
        self.assertIn("preserve and rehome the independent `## Comprehension or story visual`", skill)
        self.assertIn("A central unsupported claim cannot pass into the outline as a placeholder", skill)
        self.assertIn("**Narrow or remove the claim**", skill)
        self.assertIn("STOP and wait. Apply the selected branch explicitly", skill)
        self.assertIn("Never use this branch for a central unsupported claim", skill)
        self.assertIn("references/narrative-tension.md", skill)
        self.assertIn("Do not add a user checkpoint", skill)
        self.assertIn("question-and-resolution design", skill)
        self.assertIn("Preserve the outline's planned question, reveal timing, and resolution", skill)
        self.assertIn("Use question-and-resolution design internally", narrative)
        self.assertIn("When no genuine question emerges", narrative)
        self.assertIn("Framework role: [Answer, embodiment, application, or none.]", narrative)
        self.assertIn("whether a heading, summary, transition", critique)
        self.assertIn("answers the exact consequential question raised", article)
        self.assertIn("**Answer:**", frameworks)
        self.assertIn("**Embodiment:**", frameworks)
        self.assertIn("**Application:**", frameworks)
        self.assertIn("Do not add another user checkpoint", frameworks)
        self.assertIn("privately revalidate the article question", skill)
        self.assertIn("If the supported question disappears", skill)
        self.assertIn("remove its question-and-resolution planning lines", skill)
        self.assertIn("Before outlining, revalidate", outline)
        self.assertLess(skill.index("### 5. Check for a framework opportunity"), skill.index("### 6. Create and open the article map"))
        self.assertLess(skill.index("### 7. Follow the chosen interaction mode"), skill.index("### 8. Strengthen the proof"))
        self.assertLess(skill.index("### 8. Strengthen the proof"), skill.index("### 9. Create and approve the working outline"))
        self.assertIn("allow_implicit_invocation: false", interface)


if __name__ == "__main__":
    unittest.main()
