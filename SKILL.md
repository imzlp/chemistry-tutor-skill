---
name: chemistry-tutor
description: Analyze images or text of Chinese high-school chemistry questions and knowledge points, first asking the user to choose a target when an image contains multiple independent questions, then reconstruct the selected problem cautiously, solve it step by step, and produce a standardized Chinese response with exactly ordered sections for 题目解析、答案、知识点、易错点分析 and 教师辅助教学建议. Use for chemistry question-image OCR and interpretation, answer checking, equation derivation, concept explanation, error diagnosis, and teacher-facing instructional guidance, especially when Markdown and LaTeX rendering of formulas, chemical equations, units, charges, subscripts, equilibrium arrows, reaction conditions, or calculations must remain accurate and consistent.
---

# 高中化学试题解析

## 目标

从用户提供的题图或文字中可靠地识别条件、完成推理并输出可直接用于讲评的标准解析。优先保证化学正确性、条件完整性、格式一致性和公式可渲染性。

## 必须读取的规范

执行每次任务前读取：

- [references/output-template.md](references/output-template.md)：固定输出结构与内容要求。
- [references/markdown-latex-chemistry.md](references/markdown-latex-chemistry.md)：Markdown、LaTeX、化学方程式和单位规范。

## 工作流程

### 1. 识别题目并确定目标

1. 逐项读取题干、图表、装置、坐标轴、图例、选项、设问、单位、反应条件和手写标记。
2. **先判断图片中包含一道题还是多道相互独立的题。**“一道综合题下的（1）（2）（3）”属于同一道题的多个小问；不同题号、不同题干或彼此无关的题目属于多道独立题目。
3. 若图片包含多道独立题目，且用户没有明确指定题号、位置或题目内容，必须先列出可辨认的题号或位置并请用户确认目标题目。此时只发送简短确认问题，立即停止，不进行推理，不生成答案，也不套用五段固定输出模板。示例：“图片中包含第 8、9、10 题。请确认需要解析哪一道题？”
4. 即使用户笼统地说“解析这张图”或“分析其中的试题”，也不得默认第一题、最清晰的一题或全部题目。只有用户明确指定某一道题后，才继续解析该题。
5. 若用户已明确指定目标题号、位置或可唯一定位的题干，则直接处理该题；不得顺带解析图片中的其他独立题目。用户明确要求解析多道或全部题目时，才可按其指定范围处理。
6. 区分印刷内容与用户批注；不得默认圈选、划线或手写答案正确。
7. 对所选题目中的多个小问按原编号建立对应关系，不遗漏隐含条件，如“常温”“过量”“少量”“标准状况”“忽略体积变化”。
8. 若无法可靠判断题目边界或题号，也必须先询问用户要解析的区域，不能自行合并或拆分题目。
9. 若图片局部模糊，只陈述能确认的内容。使用“题图此处无法可靠辨认”指出位置，并给出条件化结论；禁止静默猜字、补数值或虚构选项。
10. 若题面疑似有误或答案不唯一，分别说明“按常见命题意图”和“按题面字面条件”的结论。

### 2. 建模与求解

1. 先确定考查模块：基本概念、元素化学、反应原理、电化学、平衡、实验、无机推断、有机化学、结构与性质、定量计算等。
2. 提取已知量、未知量、约束条件和守恒关系。
3. 选择最短且可检验的主方法，例如元素守恒、电荷守恒、电子守恒、质子守恒、物料守恒、关系式法、极限分析或控制变量。
4. 计算时写出“依据 → 代入 → 单位 → 结果”，保留合理有效数字。
5. 化学方程式必须检查：反应物与产物、原子守恒、电荷守恒、电子守恒、反应条件、可逆性、沉淀或气体符号。
6. 对选择题逐项判断；对实验题覆盖目的、原理、操作、现象、结论、误差与安全；对有机题覆盖官能团、反应类型、结构限制和同分异构体计数边界。
7. 完成反向核验：代回答案、数量级、单位、边界情况及题干限定是否一致。

### 3. 生成结果

严格采用 `references/output-template.md` 的五个二级标题，标题名称、顺序和数量均不得改变。不得在第一个标题前增加摘要、寒暄或“以下是解析”等文字，也不得在最后一个部分后增加额外章节。

内容原则：

- `题目解析`：呈现必要的题意重建、推理链和逐问/逐项分析，不堆砌无关知识。
- `答案`：集中给出可抄写的最终答案；与解析逐问对应。
- `知识点`：列出本题实际使用的核心知识及判定规则。
- `易错点分析`：指出具体错误、错误原因和纠正办法，不写空泛提醒。
- `教师辅助教学建议`：提供可执行的教学目标、追问、板书或活动、变式训练和评价建议。

### 4. 格式校验

输出前逐项确认：

- 五个二级标题完全一致且顺序正确。
- 行内公式使用 `$...$`，独立公式使用 `$$...$$`；不使用代码反引号包裹公式。
- 化学式的下标、离子电荷、电子、系数、箭头、条件、单位均符合规范。
- 不依赖未必启用的 `mhchem` 扩展；默认使用标准 LaTeX 的 `\mathrm{}`。
- 数学环境中不混入未经处理的中文；说明文字放在公式外。
- 不使用 Unicode 上下标字符代替 LaTeX，如 `₂`、`³⁺`。
- 表格单元格中的公式使用行内公式，避免块级公式破坏表格。

若将答案保存为 Markdown 文件，可运行：

```bash
python3 scripts/validate_chemistry_markdown.py <answer.md>
```

校验器只检查结构和常见排版错误，不能替代化学正确性复核。
