from __future__ import annotations

import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REQUIRED_FILES = ["skillpack.json", "README.md", "instructions.md"]


def init_pack(path: Path) -> int:
    path.mkdir(parents=True, exist_ok=True)
    meta = {
        "name": path.name,
        "version": "0.1.0",
        "description": "A reusable AI assistant skill pack.",
        "assistants": ["claude-code", "codex", "cursor", "copilot"],
    }
    (path / "skillpack.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (path / "README.md").write_text(f"# {path.name}\n\nInstall and usage notes.\n", encoding="utf-8")
    (path / "instructions.md").write_text("# Instructions\n\nDescribe the workflow here.\n", encoding="utf-8")
    (path / "examples").mkdir(exist_ok=True)
    print(f"Created skill pack at {path}")
    return 0


def validate_pack(path: Path) -> int:
    missing = [name for name in REQUIRED_FILES if not (path / name).exists()]
    if missing:
        print("Missing: " + ", ".join(missing))
        return 1
    try:
        meta = json.loads((path / "skillpack.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid skillpack.json: {exc}")
        return 1
    for key in ("name", "version", "description"):
        if not meta.get(key):
            print(f"Missing metadata field: {key}")
            return 1
    print("Skill pack looks good")
    return 0


def preview_pack(path: Path, port: int) -> int:
    html = path / "index.html"
    if not html.exists():
        title = path.name
        if (path / "skillpack.json").exists():
            meta = json.loads((path / "skillpack.json").read_text(encoding="utf-8"))
            title = meta.get("name", title)
        html.write_text(
            f"<!doctype html><title>{title}</title><h1>{title}</h1><p>Skill pack preview</p>",
            encoding="utf-8",
        )
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(path), **kwargs)
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"Preview serving http://127.0.0.1:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0


def export_pack(path: Path) -> int:
    if validate_pack(path) != 0:
        return 1
    installer = path / "install.sh"
    installer.write_text("#!/usr/bin/env sh\nset -eu\necho 'Install this skill pack by copying files to your assistant config.'\n", encoding="utf-8")
    print(f"Wrote {installer}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skillpack")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="scaffold a skill pack")
    init_cmd.add_argument("path", type=Path)

    validate_cmd = sub.add_parser("validate", help="validate a skill pack")
    validate_cmd.add_argument("path", type=Path)

    preview_cmd = sub.add_parser("preview", help="serve a local preview")
    preview_cmd.add_argument("path", type=Path)
    preview_cmd.add_argument("--port", type=int, default=8000)

    export_cmd = sub.add_parser("export", help="write installer files")
    export_cmd.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        return init_pack(args.path)
    if args.command == "validate":
        return validate_pack(args.path)
    if args.command == "preview":
        return preview_pack(args.path, args.port)
    if args.command == "export":
        return export_pack(args.path)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
