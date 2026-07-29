# Markdown 与 LaTeX 化学排版规范

## 1. 基本约定

- 行内公式：`$c(\mathrm{H^+})=0.10\ \mathrm{mol\,L^{-1}}$`
- 独立公式：

  ```latex
  $$
  K_a=\frac{c(\mathrm{H^+})c(\mathrm{A^-})}{c(\mathrm{HA})}
  $$
  ```

- 化学式和元素符号使用直立体 `\mathrm{}`，变量使用默认斜体。
- 默认不使用 `\ce{}`，因为部分 Markdown 渲染器未启用 `mhchem`。
- 不在公式两侧添加反引号，不用纯文本 `H2SO4` 代替正式答案中的化学式。

## 2. 化学式、离子和电子

推荐写法：

```latex
$\mathrm{H_2SO_4}$
$\mathrm{Al^{3+}}$
$\mathrm{SO_4^{2-}}$
$\mathrm{NH_4^+}$
$\mathrm{e^-}$
```

多字符电荷整体放入花括号：`\mathrm{Fe^{3+}}`、`\mathrm{CO_3^{2-}}`。

## 3. 化学方程式

### 普通反应

```latex
$$
\mathrm{2H_2 + O_2 \rightarrow 2H_2O}
$$
```

### 可逆反应和平衡

```latex
$$
\mathrm{N_2 + 3H_2 \rightleftharpoons 2NH_3}
$$
```

不要把可逆反应写成单向箭头。

### 条件标注

条件需要置于箭头上方时，将方程式拆分，避免把 `\xrightarrow` 包入 `\mathrm{}`：

```latex
$$
\mathrm{2KClO_3}
\xrightarrow{\mathrm{MnO_2},\,\Delta}
\mathrm{2KCl + 3O_2\uparrow}
$$
```

光照使用 `\xrightarrow{\text{光照}}`；通电使用 `\xrightarrow{\text{通电}}`。中文条件使用 `\text{}`。

### 沉淀、气体与状态

```latex
$\mathrm{BaSO_4\downarrow}$
$\mathrm{CO_2\uparrow}$
$\mathrm{NaCl(aq)}$
$\mathrm{H_2O(l)}$
```

仅在题意需要或反应体系中有必要区分时标注 $\uparrow$、$\downarrow$ 和状态。若反应物中已有同种气体或固体，按中学教材规范判断是否标箭头。

### 离子方程式

```latex
$$
\mathrm{Ba^{2+} + SO_4^{2-} \rightarrow BaSO_4\downarrow}
$$
```

检查左右总电荷相等。

### 电极反应

```latex
$$
\mathrm{Fe - 2e^- \rightarrow Fe^{2+}}
$$

$$
\mathrm{O_2 + 2H_2O + 4e^- \rightarrow 4OH^-}
$$
```

先根据介质判断用 $\mathrm{H^+}$、$\mathrm{OH^-}$ 或 $\mathrm{H_2O}$ 配平，再核对电子数和电荷。

### 有机结构简式

```latex
$\mathrm{CH_3CH_2OH}$
$\mathrm{CH_3COOH}$
$\mathrm{CH_2{=}CH_2}$
$\mathrm{HC{\equiv}CH}$
```

在 `\mathrm{}` 中用 `{=}` 和 `{\equiv}` 明确键符号。复杂结构若仅靠线性 LaTeX 容易歧义，应配合文字编号碳原子，不虚构二维结构图。

## 4. 数学、物理量与单位

- 物质的量：`$n(\mathrm{NaOH})=0.10\ \mathrm{mol}$`
- 浓度：`$c=0.20\ \mathrm{mol\,L^{-1}}$`
- 质量：`$m=5.85\ \mathrm{g}$`
- 摩尔质量：`$M=58.5\ \mathrm{g\,mol^{-1}}$`
- 体积：`$V=22.4\ \mathrm{L}$`
- 温度：`$25\ ^\circ\mathrm{C}$`
- 压强：`$p=101\ \mathrm{kPa}$`
- 科学计数法：`$1.8\times10^{-5}$`
- 分数：`$\dfrac{n}{V}$` 或块级公式中 `\frac{n}{V}`。

数字与单位之间保留 LaTeX 空格 `\ `；复合单位用 `\,` 连接。变量斜体，如 $n$、$m$、$V$、$K_a$；说明性下标用直立体，如 `$n_{\mathrm{总}}$`。

## 5. 多行推导

```latex
$$
\begin{aligned}
n(\mathrm{e^-})&=2n(\mathrm{Cu})\\
&=2\times0.10\ \mathrm{mol}\\
&=0.20\ \mathrm{mol}.
\end{aligned}
$$
```

`aligned` 内每行用 `\\` 换行，并在等号前放 `&` 对齐。不要在数学环境中直接写大段中文。

## 6. 语义与格式复核清单

1. 化学式下标是否完整。
2. 离子电荷的数字和正负号顺序是否正确。
3. 方程式系数是否最简整数比。
4. 原子、电荷、电子是否守恒。
5. 箭头是否反映可逆性，条件是否遗漏。
6. 气体、沉淀、状态符号是否符合题目语境。
7. 数值是否带单位，有效数字和数量级是否合理。
8. `$`、花括号、`\begin`/`\end` 是否配对。
9. 是否错误出现制表符或控制字符；尤其确保 `\frac`、`\times`、`\text` 的反斜杠完整。
10. 最终答案中的公式是否完整重现，而非只写“见上”。
