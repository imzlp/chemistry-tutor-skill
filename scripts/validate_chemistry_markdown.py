#!/usr/bin/env python3
"""Validate the fixed response structure and common chemistry LaTeX mistakes."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_HEADINGS = [
    "题目解析",
    "答案",
    "知识点",
    "易错点分析",
    "教师辅助教学建议",
]
MATH_ENVIRONMENTS = ("aligned", "array", "cases", "matrix", "pmatrix", "bmatrix")
# Deliberately broad enough for high-school chemistry/math, but restrictive enough to catch typos.
ALLOWED_COMMANDS = {
    "Delta", "Omega", "alpha", "approx", "beta", "begin", "cdot", "cdots",
    "circ", "dfrac", "downarrow", "ell", "end", "equiv", "exp", "frac", "gamma",
    "ge", "geq", "gt", "infty", "lambda", "ldots", "le", "left", "leq", "ln",
    "log", "mathrm", "mu", "neq", "nu", "omega", "overline", "partial", "pm",
    "propto", "quad", "qquad", "right", "rightleftharpoons", "rightarrow", "rho",
    "sigma", "sqrt", "sum", "text", "therefore", "theta", "times", "to", "uparrow",
    "xrightarrow",
}
UNICODE_SCRIPTS = re.compile(r"[₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]")


@dataclass(frozen=True)
class MathFragment:
    body: str
    line: int
    kind: str


def is_escaped(text: str, index: int) -> bool:
    slashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        slashes += 1
        index -= 1
    return slashes % 2 == 1


def strip_fenced_code(text: str) -> str:
    """Replace fenced-code contents with blank lines while preserving line numbers."""
    result: list[str] = []
    in_fence = False
    marker = ""
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s*(```+|~~~+)", line)
        if match:
            current = match.group(1)[0]
            if not in_fence:
                in_fence, marker = True, current
            elif current == marker:
                in_fence, marker = False, ""
            result.append("\n" if line.endswith("\n") else "")
        elif in_fence:
            result.append("\n" if line.endswith("\n") else "")
        else:
            result.append(line)
    return "".join(result)


def extract_math(text: str, errors: list[str]) -> list[MathFragment]:
    """Extract $...$ and standalone $$...$$ fragments with source line numbers."""
    fragments: list[MathFragment] = []
    outside: list[tuple[int, str]] = []
    in_block = False
    block_start = 0
    block_lines: list[str] = []

    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip() == "$$":
            if in_block:
                fragments.append(MathFragment("\n".join(block_lines), block_start, "块级公式"))
                block_lines = []
                in_block = False
            else:
                in_block = True
                block_start = lineno
            continue
        if "$$" in line:
            errors.append(f"第 {lineno} 行：块级公式分隔符 $$ 必须单独成行")
            continue
        if in_block:
            block_lines.append(line)
        else:
            outside.append((lineno, line))

    if in_block:
        errors.append(f"第 {block_start} 行起：块级公式分隔符 $$ 未闭合")

    for lineno, line in outside:
        # The fixed response format has no tables that require literal dollar signs;
        # reject obvious currency-like dollars rather than mis-pairing them as math.
        if re.search(r"(?<!\\)\$(?=\d)", line):
            errors.append(f"第 {lineno} 行：发现疑似货币符号 $；如需字面量请写成 \\$，数学内容请成对包裹")
            continue
        start: int | None = None
        index = 0
        while index < len(line):
            if line[index] == "$" and not is_escaped(line, index):
                if index + 1 < len(line) and line[index + 1] == "$":
                    index += 2
                    continue
                if start is None:
                    start = index + 1
                else:
                    fragments.append(MathFragment(line[start:index], lineno, "行内公式"))
                    start = None
            index += 1
        if start is not None:
            errors.append(f"第 {lineno} 行：行内公式分隔符 $ 未闭合；行内公式不得跨行")
    return fragments


def check_balanced(body: str, opening: str, closing: str) -> bool:
    depth = 0
    for index, char in enumerate(body):
        if is_escaped(body, index):
            continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def validate_fragment(fragment: MathFragment, errors: list[str]) -> None:
    label = f"第 {fragment.line} 行的{fragment.kind}"
    body = fragment.body
    if not body.strip():
        errors.append(f"{label}为空")
        return
    if not check_balanced(body, "{", "}"):
        errors.append(f"{label}：花括号 {{}} 未配对")
    if not check_balanced(body, "(", ")"):
        errors.append(f"{label}：小括号 () 未配对")
    if "`" in body:
        errors.append(f"{label}：数学环境中不应包含 Markdown 反引号")
    if re.search(r"\\ce\s*\{", body):
        errors.append(f"{label}：使用了依赖 mhchem 的 \\ce{{}}")
    if UNICODE_SCRIPTS.search(body):
        errors.append(f"{label}：发现 Unicode 上下标，请改用 LaTeX")
    if re.search(r"(?<!\\)\^[^\s{][+-]", body):
        errors.append(f"{label}：多字符上标应写成 ^{{...}}，例如 ^{{2-}}")
    if re.search(r"\\(?:mathrm|text|frac|dfrac|tfrac|xrightarrow|begin|end)\s+(?=\{)", body):
        errors.append(f"{label}：命令与花括号参数之间不应有空格")
    if re.search(r"\\(?:mathrm|text|frac|dfrac|tfrac|xrightarrow|begin|end)(?!\s*\{)", body):
        errors.append(f"{label}：需要花括号参数的命令缺少参数")
    if re.search(r"\\sqrt(?!\s*(?:\[[^\]]+\])?\s*\{)", body):
        errors.append(f"{label}：\\sqrt 缺少花括号参数")

    commands = re.findall(r"\\([A-Za-z]+)", body)
    unknown = sorted(set(commands) - ALLOWED_COMMANDS)
    if unknown:
        errors.append(f"{label}：发现未约定或可能拼写错误的 LaTeX 命令：{', '.join(unknown)}")

    tokens = re.findall(r"\\(begin|end)\{([^{}]+)\}", body)
    stack: list[str] = []
    mismatch = False
    for action, environment in tokens:
        if action == "begin":
            stack.append(environment)
        elif not stack or stack.pop() != environment:
            mismatch = True
            break
    if mismatch or stack:
        errors.append(f"{label}：数学环境 begin/end 的嵌套或顺序不匹配")
    begins = re.findall(r"\\begin\{([^{}]+)\}", body)
    ends = re.findall(r"\\end\{([^{}]+)\}", body)
    unsupported = sorted(set(begins + ends) - set(MATH_ENVIRONMENTS))
    if unsupported:
        errors.append(f"{label}：使用了未约定的数学环境：{', '.join(unsupported)}")

    # Common corruption: Python/string escaping turns \frac, \times or \text into tabs.
    for suffix in ("frac", "times", "text"):
        if f"\t{suffix}" in body:
            errors.append(f"{label}：疑似制表符破坏了 \\{suffix}")


def validate(text: str) -> list[str]:
    errors: list[str] = []
    headings = re.findall(r"^## (.+?)\s*$", text, flags=re.MULTILINE)
    if headings != REQUIRED_HEADINGS:
        errors.append(f"二级标题必须严格为 {REQUIRED_HEADINGS}，实际为 {headings}")

    if re.search(r"```(?:latex|math)\b", text, flags=re.IGNORECASE):
        errors.append("最终答案不应把待渲染公式放入 latex/math 代码围栏")

    scan_text = strip_fenced_code(text)
    fragments = extract_math(scan_text, errors)
    for fragment in fragments:
        validate_fragment(fragment, errors)
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_chemistry_markdown.py <answer.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Cannot read {path}: {exc}", file=sys.stderr)
        return 2

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
