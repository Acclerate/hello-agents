#!/usr/bin/env python3
"""校验 kb/ 知识库内的 wikilink 与 canvas 引用是否全部可解析。

用法：
    python scripts/check_kb_links.py

规则：
- `[[目标]]` / `[[目标|别名]]` / `[[目标#标题]]` / `![[嵌入]]` 均按 basename（不含扩展名）解析，
  与 Obsidian「最短路径」链接策略一致；同名 basename 且未写路径视为冲突。
- 代码块与行内代码中的 [[...]] 不参与解析（Obsidian 同样不解析），自动跳过。
- canvas 中 file 节点的路径必须精确存在。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = (".git", ".obsidian", ".zcode", "__pycache__", "node_modules")


def build_index() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    stems: dict[str, list[str]] = {}
    basenames: dict[str, list[str]] = {}
    for p in ROOT.rglob("*"):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel.split("/")[0] in EXCLUDE_DIRS:
            continue
        if p.suffix in (".md", ".canvas", ".base"):
            stems.setdefault(p.stem, []).append(rel)
            stems.setdefault(p.name, []).append(rel)  # 带扩展名的链接（![[xx.base]]）
            basenames.setdefault(p.name, []).append(rel)
    return stems, basenames


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def check() -> int:
    stems, basenames = build_index()
    errors: list[str] = []
    checked = 0

    for note in sorted((ROOT / "kb").rglob("*.md")):
        text = strip_code(note.read_text(encoding="utf-8"))
        for m in re.finditer(r"!?\[\[([^\]]+)\]\]", text):
            inner = m.group(1)
            target = re.split(r"\\\||\|", inner)[0].strip()
            target = target.split("#")[0].strip()
            if not target:
                continue
            checked += 1
            stem = target.split("/")[-1]
            if stem not in stems:
                errors.append(f"{note.relative_to(ROOT)} -> [[{target}]]（无法解析）")
            elif len(stems[stem]) > 1 and "/" not in target:
                errors.append(f"{note.relative_to(ROOT)} -> [[{target}]]（basename 冲突: {stems[stem]}）")

    for cv in (ROOT / "kb").rglob("*.canvas"):
        for node in json.loads(cv.read_text(encoding="utf-8")).get("nodes", []):
            if node.get("type") == "file":
                checked += 1
                name = node["file"].split("/")[-1]
                if node["file"] not in basenames.get(name, []):
                    errors.append(f"{cv.relative_to(ROOT)} -> canvas 节点文件不存在: {node['file']}")

    print(f"检查 wikilink/canvas 引用 {checked} 处")
    if errors:
        print(f"✗ {len(errors)} 处失效：")
        for e in errors:
            print("  -", e)
        return 1
    print("✓ 全部解析成功")
    return 0


if __name__ == "__main__":
    sys.exit(check())
