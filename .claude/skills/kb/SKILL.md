---
name: kb
description: |
  LLM 驱动的知识库管理工具箱。当用户说"kb"、"知识库"、"查知识库"、"初始化知识库"、"导入文件"、"编译"、"回填"等时触发。
  支持对 vault 或外部目录建立知识库：预处理文件、编译 wiki、查询分析、健康检查。
  基于 Karpathy 的 LLM Knowledge Base 模式：raw/ 存原始资料，LLM 编译成 wiki/，索引替代 RAG。
user-invocable: true
---

# /kb — LLM 知识库管理

统一入口，包含 7 个子命令。

## 子命令速查

| 命令 | 功能 | 触发词 |
|------|------|--------|
| `kb init [目录]` | 初始化知识库 | "初始化"、"创建知识库" |
| `kb ingest` | 预处理 raw/ 文件 | "导入"、"处理新文件" |
| `kb compile [文件]` | 编译为 wiki | "编译"、"更新 wiki" |
| `kb query "<问题>"` | 查询知识库 | "查知识库"、"问知识库" |
| `kb file [报告]` | 回填到 wiki | "回填"、"归档" |
| `kb lint` | 健康检查 | "检查"、"lint" |
| `kb status` | 状态仪表盘 | "状态"、"看看知识库" |

---

## kb init [目标目录]

初始化知识库目录结构、索引和本体定义。

**参数**：可选目标目录，默认当前目录（vault）或指定外部目录。

### 执行步骤

1. **检查现有知识库**：查找 `{target}/index/MASTER-INDEX.md`，如果存在则警告并等待确认

2. **创建目录结构**：
   ```
   {target}/raw/              — 原始资料（只读）
   {target}/wiki/concepts/    — 核心概念
   {target}/wiki/sources/     — 来源摘要
   {target}/wiki/comparisons/ — 对比分析
   {target}/output/analysis/  — 分析报告
   {target}/output/slides/     — 幻灯片
   {target}/index/            — 索引文件
   {target}/scripts/           — 预处理脚本
   ```

3. **复制模板文件**：从本 Skill 的 `templates/` 目录复制到 `{target}/index/`：
   - ONTOLOGY.md — 实体类型和关系定义
   - MASTER-INDEX.md — 全局索引
   - TOPIC-MAP.md — 主题分组
   - RAW-REGISTRY.md — 原始文件登记

4. **复制脚本**：从本 Skill 的 `scripts/` 目录复制到 `{target}/scripts/`

5. **检查 Python 依赖**：
   ```bash
   pip show pymupdf openpyxl pandas pytesseract python-docx Pillow 2>&1
   ```
   报告缺失的包，询问是否安装

6. **配置 SessionStart Hook（可选）**：询问是否配置，检测 raw/ 新文件时提醒

7. **输出初始化摘要**

---

## kb ingest

预处理 raw/ 中的新文件并登记到索引。

**前置条件**：知识库已初始化（存在 index/RAW-REGISTRY.md）

### 支持格式
- PDF (.pdf)
- Excel (.xlsx, .xls, .csv)
- 图片 (.png, .jpg, .jpeg) — OCR 提取
- Word (.docx)

### 执行步骤

1. **定位知识库**：向上查找 `index/RAW-REGISTRY.md`

2. **运行预处理脚本**：
   ```bash
   python3 {skill_dir}/scripts/ingest.py {kb_root}
   ```
   脚本自动：扫描新文件 → 按类型提取文本 → 输出摘要

3. **登记到 RAW-REGISTRY.md**：为每个新文件添加条目：
   - 文件路径、类型、摘要（一句话）
   - 状态：`pending`（待编译）

4. **输出摘要**：报告导入数量，提示下一步 `/kb-compile`

---

## kb compile [文件]

将 raw/ 中已导入但未编译的文件编译为 wiki 文章。

**参数**：可选指定文件，默认处理所有 `status=pending` 的条目

### 核心原则
- Wiki 文章由 LLM 生成，遵循 ONTOLOGY.md 定义
- 每篇文章必须有完整 YAML frontmatter
- 使用 `[[双链]]` 建立关联
- 编译是增量的

### 执行步骤

1. **检查待编译条目**：读 `index/RAW-REGISTRY.md`，找 `status=pending` 的条目
   - 如果没有，告知用户并结束

2. **加载上下文**：读 ONTOLOGY.md、MASTER-INDEX.md、TOPIC-MAP.md

3. **逐个编译**：
   - 读取源文件或 `raw/.extracted/` 下的提取文本
   - 判断操作：新建 / 更新已有 / 综合分析
   - 按模板生成 wiki 文章
   - 更新 frontmatter（type, id, compiled_from, related, last_compiled）
   - 用 `[[双链]]` 链接相关文章

4. **更新索引**：
   - MASTER-INDEX.md 添加/更新条目
   - TOPIC-MAP.md 归入主题
   - RAW-REGISTRY.md 状态改为 `done`，填编译产物路径

5. **输出编译摘要**

---

## kb query "<问题>"

对知识库提问，生成结构化报告。

**参数**：必填，用户的问题

### 执行步骤

1. **定位知识库**：查找 `index/MASTER-INDEX.md`

2. **检索相关文章**：
   - 读 MASTER-INDEX.md 定位相关文件
   - 按需读 TOPIC-MAP.md 精确定位
   - 读取所有相关 wiki 文章内容

3. **研究分析**：
   - 基于 wiki 内容深入分析问题
   - 交叉对比多篇文章
   - 结论必须基于实际内容，标注来源

4. **生成报告**：保存到 `output/analysis/YYYY-MM-DD-{topic-slug}.md`：
   ```markdown
   # {报告标题}

   - **Date**: YYYY-MM-DD
   - **Query**: {用户问题}
   - **Sources**: {引用的 wiki 文章}

   ---

   ## 分析
   {详细分析，引用具体文章用 [[双链]]}

   ## 结论
   {核心发现}

   ## 回填建议
   - [ ] {具体建议}
   ```

5. **输出结果**：展示摘要，提示可运行 `/kb file` 回填

---

## kb file [报告路径]

将查询输出回填到 wiki 知识库。

**参数**：可选指定 output/ 下的报告文件，默认扫描 `output/analysis/`

### 执行步骤

1. **定位知识库和待回填内容**

2. **展示回填建议**：列出所有建议，编号说明

3. **用户确认**：逐条 Y/N 或批量操作

4. **执行回填**：
   - **更新已有文章**：将新内容有机融入
   - **新建文章**：按 ONTOLOGY.md 模板创建

5. **更新索引**：MASTER-INDEX.md 和 TOPIC-MAP.md

6. **输出摘要**

---

## kb lint

对知识库进行六项健康检查。

### 检查项目

| 检查 | 说明 |
|------|------|
| 断链 | `[[链接]]` 指向不存在的文件 |
| 孤岛 | 没有被任何文章链接的文章 |
| 溯源 | frontmatter compiled_from 指向已删除的文件 |
| 一致性 | 同一概念在不同文章中的矛盾描述 |
| 覆盖度 | 未编译文件比例 |
| 空白发现 | 被提及但没有独立文章的概念 |

### 执行步骤

1. **定位知识库**

2. **执行六项检查**

3. **输出 Lint 报告**（按严重程度排序）

4. **提供修复选项**：可自动修复的问题询问是否执行

5. **保存报告到 `index/LINT-REPORT.md`**

---

## kb status

展示知识库整体状态仪表盘。

### 执行步骤

1. **定位知识库**

2. **收集统计数据**：
   - raw/ 文件数
   - wiki/ 文章数和字数
   - 编译率
   - 待回填报告数
   - 上次 lint 结果

3. **展示仪表盘**：
   ```
   知识库状态
   ═══════════════════════════════════
   原始文件:    N 个
   Wiki 文章:   M 篇 (共 ~X 字)
   编译率:      XX%
   待回填:      Y 份报告
   上次 Lint:   日期 — 问题摘要
   ═══════════════════════════════════

   最近编译的文章:
     - wiki/concepts/xxx.md (日期)

   待处理:
     - N 个文件待编译 → /kb compile
     - M 份报告待回填 → /kb file
   ```

4. **建议下一步操作**

---

## 目录结构约定

```
{知识库根目录}/
├── raw/                    # 原始资料（只读）
│   └── .extracted/         # 提取的文本（自动生成）
├── wiki/
│   ├── concepts/           # 核心概念
│   ├── sources/            # 来源摘要
│   └── comparisons/        # 对比分析
├── output/
│   ├── analysis/           # 查询报告
│   └── slides/             # 幻灯片
├── index/
│   ├── MASTER-INDEX.md     # 全局索引
│   ├── TOPIC-MAP.md        # 主题分组
│   ├── RAW-REGISTRY.md     # 原始文件登记
│   ├── LINT-REPORT.md      # 健康检查报告
│   └── ONTOLOGY.md         # 本体定义
└── scripts/
    ├── ingest.py           # 预处理脚本
    ├── requirements.txt    # Python 依赖
    └── extractors/         # 各类文件提取器
```

## 实体类型（ONTOLOGY.md）

| 类型 | 目录 | 命名规则 |
|------|------|----------|
| concept | wiki/concepts/ | {slug}.md |
| source | wiki/sources/ | {slug}.md |
| comparison | wiki/comparisons/ | {a}-vs-{b}.md |

## Wiki 文章 Frontmatter 模板

```yaml
---
type: concept
id: {slug}
aliases: []
compiled_from:
  - raw/{source_file}
related:
  - "[[other-article]]"
last_compiled: YYYY-MM-DD
---
```

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 找不到知识库 | 先运行 `/kb init` 初始化 |
| 脚本报错 | 运行 `pip install -r scripts/requirements.txt` |
| 编译率低 | 运行 `/kb ingest` 导入新文件，然后 `/kb compile` |
| 断链太多 | 运行 `/kb lint` 查看详情，手动修复或删除断链 |
