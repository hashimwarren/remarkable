#!/usr/bin/env python3
"""Preflight and run Slopless, acquiring a pinned CLI through npx when needed."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
from pathlib import Path


SLOPLESS_VERSION = "0.2.23"
NPX_PACKAGE = f"slopless@{SLOPLESS_VERSION}"


def find_installed_command(project_root: Path) -> list[str] | None:
    names = ["slopless.cmd", "slopless"] if os.name == "nt" else ["slopless"]
    for name in names:
        local = project_root / "node_modules" / ".bin" / name
        if local.is_file() and (os.name == "nt" or os.access(local, os.X_OK)):
            return [str(local)]
    global_command = shutil.which("slopless")
    return [global_command] if global_command else None


def find_npx_command() -> str | None:
    names = ["npx.cmd", "npx"] if os.name == "nt" else ["npx"]
    for name in names:
        command = shutil.which(name)
        if command:
            return command
    return None


def resolve_command(project_root: Path) -> tuple[list[str] | None, str | None]:
    installed = find_installed_command(project_root)
    if installed:
        return installed, "installed"
    npx = find_npx_command()
    if npx:
        return [npx, "--yes", NPX_PACKAGE], "npx"
    return None, None


def emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2))


def collect_messages(payload: object) -> list[dict[str, object]]:
    """Collect textlint messages from both wrapped and flat Slopless JSON."""
    messages: list[dict[str, object]] = []
    if isinstance(payload, list):
        for item in payload:
            messages.extend(collect_messages(item))
    elif isinstance(payload, dict):
        if isinstance(payload.get("ruleId"), str):
            messages.append(payload)
        else:
            for key in ("messages", "results", "findings"):
                if key in payload:
                    messages.extend(collect_messages(payload[key]))
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", nargs="?", help="Markdown file to lint")
    parser.add_argument("--preflight", action="store_true", help="Verify Slopless is runnable without linting")
    parser.add_argument("--project-root", default=".", help="Project containing Slopless")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.is_dir():
        parser.error(f"not a directory: {project_root}")
    if not args.preflight and not args.draft:
        parser.error("draft is required unless --preflight is used")
    draft = Path(args.draft).expanduser().resolve() if args.draft else None
    if draft is not None:
        if not draft.is_file():
            parser.error(f"not a file: {draft}")
        if draft.suffix.casefold() not in {".md", ".mdx"}:
            parser.error("Slopless input must be Markdown")

    command, source = resolve_command(project_root)
    if command is None:
        emit(
            {
                "status": "blocked",
                "stage": "resolve",
                "message": "Slopless is not installed and npx is unavailable. Node.js 22.13.0 or newer is required.",
                "required_package": NPX_PACKAGE,
            }
        )
        return 2

    try:
        help_run = subprocess.run(
            [*command, "--help"],
            cwd=project_root,
            text=True,
            capture_output=True,
            timeout=min(args.timeout, 30),
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        emit({"status": "blocked", "stage": "help", "source": source, "message": str(error)})
        return 2
    if help_run.returncode != 0:
        emit(
            {
                "status": "blocked",
                "stage": "help",
                "source": source,
                "exit_code": help_run.returncode,
                "stderr": help_run.stderr.strip(),
                "message": "Could not acquire or execute the pinned Slopless CLI.",
            }
        )
        return 2

    if args.preflight:
        emit(
            {
                "status": "ready",
                "source": source,
                "package": NPX_PACKAGE if source == "npx" else None,
            }
        )
        return 0

    assert draft is not None

    try:
        lint_run = subprocess.run(
            [*command, str(draft)],
            cwd=project_root,
            text=True,
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        emit({"status": "error", "stage": "lint", "message": str(error)})
        return 2

    raw = lint_run.stdout.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as error:
        emit(
            {
                "status": "error",
                "stage": "parse",
                "exit_code": lint_run.returncode,
                "message": f"Slopless did not return JSON: {error}",
                "stderr": lint_run.stderr.strip(),
            }
        )
        return 2

    messages = collect_messages(parsed)
    rule_ids = sorted(
        {
            rule_id
            for message in messages
            if isinstance((rule_id := message.get("ruleId")), str)
        }
    )

    findings_dir = project_root / ".slopless" / "findings"
    findings_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    output = findings_dir / f"{stamp}--{draft.stem}.json"
    output.write_text(raw + "\n", encoding="utf-8")

    if lint_run.returncode == 0:
        status = "clean"
    elif lint_run.returncode == 1:
        status = "findings"
    else:
        emit(
            {
                "status": "error",
                "stage": "lint",
                "exit_code": lint_run.returncode,
                "findings_path": str(output),
                "stderr": lint_run.stderr.strip(),
            }
        )
        return 2

    emit(
        {
            "status": status,
            "source": source,
            "exit_code": lint_run.returncode,
            "draft": str(draft),
            "finding_count": len(messages),
            "rule_type_count": len(rule_ids),
            "rule_ids": rule_ids,
            "findings_path": str(output),
            "stderr": lint_run.stderr.strip(),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
