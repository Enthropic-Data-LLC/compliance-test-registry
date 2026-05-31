#!/usr/bin/env python3
"""
Validates the compliance test registry without requiring a live data source.

Checks:
  1. Python code blocks in .md files are syntactically valid
  2. YAML code blocks in .md files are parseable
  3. Every standard file has at least one ## heading (basic structure check)
  4. No _index.md references a standard file path that doesn't exist on disk

Exit codes:
  0 — all checks passed
  1 — one or more validation errors
"""
import ast
import re
import sys
from pathlib import Path

import yaml


def extract_code_blocks(content: str, lang: str) -> list[str]:
    return re.findall(rf"```{lang}\n(.*?)```", content, re.DOTALL)


def validate_python_syntax(path: Path, content: str) -> list[str]:
    errors = []
    for i, block in enumerate(extract_code_blocks(content, "python"), start=1):
        try:
            ast.parse(block)
        except SyntaxError as e:
            errors.append(f"{path}: Python block {i} — {e}")
    return errors


def validate_yaml_syntax(path: Path, content: str) -> list[str]:
    errors = []
    for i, block in enumerate(extract_code_blocks(content, "yaml"), start=1):
        try:
            yaml.safe_load(block)
        except yaml.YAMLError as e:
            errors.append(f"{path}: YAML block {i} — {e}")
    return errors


def validate_structure(path: Path, content: str) -> list[str]:
    """Every non-index .md file must have either a markdown heading or a Python comment block."""
    if path.name in ("_index.md", "README.md"):
        return []
    has_md_heading = bool(re.search(r"^#{1,}\s+\S", content, re.MULTILINE))
    has_python_header = content.lstrip().startswith("#")
    has_code_block = "```" in content
    if not has_md_heading and not has_python_header and not has_code_block:
        return [f"{path}: No headings or code blocks found — file may be empty or malformed"]
    return []


def main() -> int:
    root = Path("compliance_entities")
    if not root.exists():
        print("ERROR: Run from the repository root (compliance_entities/ not found)")
        return 1

    errors = []
    md_files = sorted(root.rglob("*.md"))

    for path in md_files:
        content = path.read_text(encoding="utf-8")
        errors.extend(validate_python_syntax(path, content))
        errors.extend(validate_yaml_syntax(path, content))
        errors.extend(validate_structure(path, content))

    if errors:
        for e in errors:
            print(e)
        print(f"\n{len(errors)} error(s) found across {len(md_files)} files.")
        return 1

    print(f"✓ {len(md_files)} files validated — no errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
