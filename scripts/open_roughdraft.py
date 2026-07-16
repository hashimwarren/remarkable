#!/usr/bin/env python3
"""Open a Markdown draft in Roughdraft and optionally wait for Done Reviewing."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


INSTALL_COMMAND = "npm i -g roughdraft"


def find_command(project_root: Path) -> str | None:
    names = ["roughdraft.cmd", "roughdraft"] if os.name == "nt" else ["roughdraft"]
    for name in names:
        local = project_root / "node_modules" / ".bin" / name
        if local.is_file() and (os.name == "nt" or os.access(local, os.X_OK)):
            return str(local)
    return shutil.which("roughdraft")


def emit(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2))


def review_event(output: str) -> dict[str, object] | None:
    """Return the last JSON review event emitted by Roughdraft."""
    event: dict[str, object] | None = None
    for line in output.splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            event = payload
    return event


def review_status(event: dict[str, object] | None) -> str:
    if event is None:
        return "review_ended"
    name = str(event.get("event", event.get("status", ""))).casefold().replace("_", ".").replace("-", ".")
    if name in {"review.completed", "completed"}:
        return "review_completed"
    if name in {"review.abandoned", "review.cancelled", "review.canceled", "review.closed", "abandoned", "cancelled", "canceled"}:
        return "review_abandoned"
    return "review_ended"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", help="Markdown file to open")
    parser.add_argument("--project-root", default=".", help="Project root for local binaries")
    parser.add_argument("--no-watch", action="store_true", help="Open and return without waiting for review")
    parser.add_argument("--timeout", type=int, help="Optional review timeout in seconds")
    args = parser.parse_args()

    draft = Path(args.draft).expanduser().resolve()
    project_root = Path(args.project_root).expanduser().resolve()
    if not draft.is_file():
        parser.error(f"not a file: {draft}")
    if draft.suffix.casefold() not in {".md", ".mdx"}:
        parser.error("Roughdraft input must be Markdown")
    if not project_root.is_dir():
        parser.error(f"not a directory: {project_root}")

    command = find_command(project_root)
    if command is None:
        emit(
            {
                "status": "missing",
                "install_command": INSTALL_COMMAND,
                "help_command": "roughdraft --help",
                "draft": str(draft),
            }
        )
        return 0

    help_text = ""
    for help_args in ([command, "--help"], [command, "open", "--help"]):
        try:
            result = subprocess.run(
                help_args,
                cwd=project_root,
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            emit({"status": "error", "stage": "help", "message": str(error)})
            return 2
        help_text += "\n" + result.stdout + "\n" + result.stderr
        if result.returncode not in {0, 2}:
            emit(
                {
                    "status": "error",
                    "stage": "help",
                    "exit_code": result.returncode,
                    "stderr": result.stderr.strip(),
                }
            )
            return 2

    if "--no-watch" not in help_text:
        emit(
            {
                "status": "unsupported",
                "message": "Installed Roughdraft does not advertise the required review modes; update it before using the beta handoff.",
                "install_command": INSTALL_COMMAND,
            }
        )
        return 0
    if not args.no_watch and "--json" not in help_text:
        emit(
            {
                "status": "unsupported",
                "message": "Installed Roughdraft does not advertise JSON review events; update it before using watched review.",
                "install_command": INSTALL_COMMAND,
            }
        )
        return 0

    open_args = [command, "open", str(draft)]
    if args.no_watch:
        open_args.append("--no-watch")
    if not args.no_watch and args.timeout is not None:
        open_args.extend(["--timeout", str(args.timeout)])
    if "--json" in help_text:
        open_args.append("--json")
    try:
        opened = subprocess.run(
            open_args,
            cwd=project_root,
            text=True,
            capture_output=True,
            timeout=None if args.timeout is None else args.timeout + 5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        emit({"status": "error", "stage": "open", "message": str(error)})
        return 2
    if opened.returncode != 0:
        emit(
            {
                "status": "error",
                "stage": "open",
                "exit_code": opened.returncode,
                "stderr": opened.stderr.strip(),
            }
        )
        return 2

    event = None if args.no_watch else review_event(opened.stdout)
    status = "opened" if args.no_watch else review_status(event)
    emit(
        {
            "status": status,
            "watching": not args.no_watch,
            "draft": str(draft),
            "command": open_args,
            "review_event": event,
            "output": opened.stdout.strip(),
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
