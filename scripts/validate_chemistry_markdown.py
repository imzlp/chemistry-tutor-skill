#!/usr/bin/env python3
"""Validate the fixed section structure and common LaTeX mistakes in chemistry Markdown."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = [
    "题目解析",
    "答案",
    "知识点",
    "易错点分析",
    "教师辅助教学建议",
]


def validate(text: str) -> list[str]:
    errors: list[str] = []
    headings = re.findall(r"^## (.+?)\s*$", text, flags=re.MULTILINE)
    if headings != REQUIRED:
        errors.append(f"二级标题必须严格为 {REQUIRED}，实际为 {headings}")

    if text.count("$$") % 2:
        errors.append("块级公式分隔符 $$ 未成对")

    without_blocks = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    if len(re.findall(r"(?<!\\)\$", without_blocks)) % 2:
        errors.append("行内公式分隔符 $ 未成对")

    unicode_scripts = re.findall(r"[₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]", text)
    if unicode_scripts:
        errors.append("发现 Unicode 上下标，请改用 LaTeX 下标/上标")

    for bad, label in [("\tfrac", "疑似制表符破坏了 \\frac"), ("\times", "疑似制表符破坏了 \\times"), ("\text", "疑似制表符破坏了 \\text")]:
        if bad in text:
            errors.append(label)

    if "```latex" in text or "```math" in text:
        errors.append("最终答案不应把待渲染公式放入代码围栏")

    for env in ("aligned", "array", "cases"):
        if text.count(rf"\begin{{{env}}}") != text.count(rf"\end{{{env}}}"):
            errors.append(f"{env} 环境的 begin/end 未配对")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_chemistry_markdown.py <answer.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors = validate(text)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
