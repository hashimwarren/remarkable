#!/usr/bin/env python3
"""Focused tests for Remarkable's deterministic helpers and instruction contract."""

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
        self.assertIn("1.2.1", skill)
        self.assertIn("five-scout premise council", transformation)
        scout_preamble = transformation.split("Before delegation, tell the writer:", 1)[1].split(
            "Give every scout", 1
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


class ArticleRouteInstructionTests(unittest.TestCase):
    def test_two_advocated_routes_gate_outline_and_proof(self) -> None:
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        routes = (SKILL_DIR / "references" / "article-routes.md").read_text(
            encoding="utf-8"
        )

        self.assertEqual(routes.count("### A. [Concrete route name]"), 1)
        self.assertEqual(routes.count("### B. [Concrete route name]"), 1)
        self.assertNotIn("### C. [Concrete route name]", routes)
        self.assertIn("Present exactly:", routes)
        self.assertIn("Advocate for both routes", routes)
        self.assertIn("Which direction should govern the outline: A or B?", routes)
        self.assertIn("STOP and wait", routes)
        self.assertIn("combination, revision, or another direction", routes)
        self.assertIn("reconfirm the revised route before outlining", routes)
        self.assertIn("Do not create a separate route artifact", routes)
        self.assertIn("Create the working outline directly from this brief", routes)

        route_stage = skill.index("5. **Article route.**")
        outline_stage = skill.index("6. **Working outline.**")
        proof_stage = skill.index("7. **Proof.**")
        approval_stage = skill.index("8. **Outline approval.**")
        self.assertLess(route_stage, outline_stage)
        self.assertLess(outline_stage, proof_stage)
        self.assertLess(proof_stage, approval_stage)
        self.assertIn("reserve_draft.py", self.read_outline())

    def test_visual_generation_waits_for_stable_proof(self) -> None:
        prove = (SKILL_DIR / "references" / "prove.md").read_text(encoding="utf-8")
        visuals = (SKILL_DIR / "references" / "visual-placeholders.md").read_text(encoding="utf-8")
        self.assertIn("After claim and section jobs are stable", prove)
        self.assertIn("dedicated visual subagent", prove)
        self.assertIn("spawn one dedicated visual subagent", visuals)

    @staticmethod
    def read_outline() -> str:
        return (SKILL_DIR / "references" / "outline.md").read_text(encoding="utf-8")


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
    STAGE_OWNERS = (
        "premise.md",
        "premise-transformation.md",
        "objection-response.md",
        "personal-authority.md",
        "framework-design.md",
        "article-routes.md",
        "outline.md",
        "prove.md",
        "article.md",
        "critique.md",
        "roughdraft-handoff.md",
        "slopless.md",
    )
    CONTRACT_HEADINGS = (
        "## Purpose",
        "## Required inputs",
        "## Process",
        "## User checkpoint",
        "## Artifact or state effects",
        "## Degraded and failure behavior",
        "## Completion criterion",
        "## Next-stage handoff",
    )

    def read(self, relative_path: str) -> str:
        return (SKILL_DIR / relative_path).read_text(encoding="utf-8")

    def test_router_is_low_resolution_and_all_pointers_resolve(self) -> None:
        skill = self.read("SKILL.md")
        self.assertLess(len(skill.splitlines()), 120)
        self.assertLess(len(skill.split()), 1600)
        for target in re.findall(r"\\]\\((references/[^)]+\\.md)\\)", skill):
            self.assertTrue((SKILL_DIR / target).is_file(), target)
        for owner in self.STAGE_OWNERS:
            self.assertIn(f"references/{owner}", skill)

    def test_every_stage_owner_uses_the_shared_contract_shape(self) -> None:
        for owner in self.STAGE_OWNERS:
            content = self.read(f"references/{owner}")
            positions = [content.index(heading) for heading in self.CONTRACT_HEADINGS]
            self.assertEqual(positions, sorted(positions), owner)

    def test_detailed_contracts_live_outside_the_router(self) -> None:
        skill = self.read("SKILL.md")
        premise = self.read("references/premise.md")
        objection = self.read("references/objection-response.md")
        framework = self.read("references/framework-design.md")
        routes = self.read("references/article-routes.md")
        outline = self.read("references/outline.md")
        prove = self.read("references/prove.md")
        critique = self.read("references/critique.md")
        roughdraft = self.read("references/roughdraft-handoff.md")
        slopless = self.read("references/slopless.md")

        self.assertNotIn("Who’s this for?", skill)
        self.assertIn("Who’s this for? What should they see differently", premise)
        self.assertNotIn("Yes — I’ll answer", skill)
        self.assertIn("Yes — I’ll answer", objection)
        self.assertNotIn("Develop the framework", skill)
        self.assertIn("Develop the framework", framework)
        self.assertNotIn("Which direction should govern the outline", skill)
        self.assertIn("Which direction should govern the outline", routes)
        self.assertNotIn("Draft this structure", skill)
        self.assertIn("Draft this structure", outline)
        self.assertNotIn("Narrow or remove the claim", skill)
        self.assertIn("Narrow or remove the claim", prove)
        self.assertNotIn("Run Remarkable critique", skill)
        self.assertIn("Run Remarkable critique", critique)
        self.assertNotIn("click **Done Reviewing**", skill)
        self.assertIn("click **Done Reviewing**", roughdraft)
        self.assertNotIn("run_slopless.py --preflight", skill)
        self.assertIn("run_slopless.py --preflight", slopless)

    def test_lifecycle_order_and_completion_gates_are_explicit(self) -> None:
        skill = self.read("SKILL.md")
        labels = (
            "1. **Premise.**",
            "2. **Objection.**",
            "3. **Personal Authority.**",
            "4. **Framework.**",
            "5. **Article route.**",
            "6. **Working outline.**",
            "7. **Proof.**",
            "8. **Outline approval.**",
            "9. **Draft.**",
            "10. **Slopless.**",
            "11. **Critique and review.**",
        )
        positions = [skill.index(label) for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertGreaterEqual(skill.count("Complete when"), 7)
        self.assertIn("Complete only when", skill)
        self.assertIn("Complete on a clean result", skill)
        self.assertIn("Resume at the earliest unmet observable completion condition", skill)

    def test_durable_artifact_ownership_is_single_and_bounded(self) -> None:
        skill = self.read("SKILL.md")
        premise = self.read("references/premise.md")
        context = self.read("references/context-artifacts.md")
        self.assertEqual(premise.count("# Premise\n\nDraft:"), 1)
        self.assertNotIn("# Premise\n\nDraft:", skill)
        self.assertNotIn("appeal, and fascination", context)
        self.assertIn("only durable stores of article decisions", skill)
        self.assertIn("Do not create a route artifact", self.read("references/article-routes.md"))
        self.assertIn("Create no separate proof artifact", self.read("references/prove.md"))
        self.assertIn("create a separate framework artifact", self.read("references/framework-design.md"))

    def test_roughdraft_contract_is_watched_and_recoverable(self) -> None:
        handoff = self.read("references/roughdraft-handoff.md")
        self.assertIn("--no-watch", handoff)
        self.assertIn("review_completed", handoff)
        for status in ("missing", "unsupported", "error", "review_ended", "review_abandoned"):
            self.assertIn(status, handoff)
        self.assertIn("Review completion alone never", handoff)
        self.assertIn("chat/Markdown fallback", handoff)

    def test_slopless_contract_preserves_transparency_and_failure_gate(self) -> None:
        slopless = self.read("references/slopless.md")
        self.assertIn("slopless@0.2.23", slopless)
        self.assertIn("Never silently produce an unlinted English article", slopless)
        self.assertIn("It flagged [initial count] issues", slopless)
        self.assertIn("ran Slopless [run count] times in total", slopless)
        self.assertIn("deliberate exceptions", slopless)
        self.assertIn("non-English", slopless)

    def test_premise_divergence_and_existing_product_contracts_survive(self) -> None:
        premise = self.read("references/premise.md")
        transformation = self.read("references/premise-transformation.md")
        personal = self.read("references/personal-authority.md")
        framework = self.read("references/framework-design.md")
        routes = self.read("references/article-routes.md")
        outline = self.read("references/outline.md")
        prove = self.read("references/prove.md")
        article = self.read("references/article.md")
        critique = self.read("references/critique.md")

        self.assertIn("exactly three", premise)
        self.assertIn("## [A, B, or C]. [Distinctive direction name]", premise)
        self.assertIn("Go wider", premise)
        self.assertIn("five assigned scouts", transformation)
        self.assertIn("capacity-aware waves", transformation)
        self.assertIn("Audience frame", transformation)
        self.assertIn("worldview fit, language fit, generative power", transformation)
        self.assertIn("whole-article test", transformation)
        self.assertIn("pairwise", transformation)
        self.assertIn("Earned Discovery", personal)
        self.assertIn("Shared Struggle", personal)
        self.assertIn("Transformation", personal)
        self.assertIn("Whole / Parts / Whole", framework)
        self.assertIn("Decision Tree", framework)
        self.assertIn("PAS — Problem, Agitate, Solve", routes)
        self.assertIn("exactly two", routes)
        self.assertIn("300–700", outline)
        self.assertIn("reserve_outline.py", outline)
        self.assertIn("Status: approved", outline)
        self.assertIn("central unsupported claim to pass as a placeholder", prove)
        self.assertIn("800–1,200", article)
        self.assertIn("Never invent", article)
        self.assertIn("Review revisions one by one", critique)
        self.assertIn("Apply recommended revisions", critique)
        self.assertIn("Leave the draft unchanged", critique)

    def test_retired_map_and_invocation_contracts(self) -> None:
        skill = self.read("SKILL.md")
        outline = self.read("references/outline.md")
        interface = self.read("agents/openai.yaml")
        self.assertNotIn("create_article_map.py", skill)
        self.assertNotIn("create_article_map.py", outline)
        self.assertIn("legacy map", outline)
        self.assertIn("Use only when a human explicitly invokes Remarkable", skill)
        self.assertIn("allow_implicit_invocation: false", interface)


if __name__ == "__main__":
    unittest.main()
