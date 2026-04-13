# /kb — LLM 知识库管理工具

基于 Karpathy 的 LLM Knowledge Base 模式：raw/ 存原始资料，LLM 编译成 wiki/，索引替代 RAG。

## 快速开始

### 1. 初始化知识库

```
/kb init
```

在当前目录创建知识库目录结构：
- `raw/` — 原始资料（只读）
- `wiki/concepts/` — 核心概念
- `wiki/sources/` — 来源摘要
- `wiki/comparisons/` — 对比分析
- `output/analysis/` — 分析报告
- `output/slides/` — 幻灯片
- `index/` — 索引文件

### 2. 导入文件

将 PDF、Excel、图片、Word 文档放入 `raw/` 目录，然后：

```
/kb ingest
```

自动提取文本并登记到索引。

### 3. 编译为 Wiki

```
/kb compile
```

LLM 读取原料，生成结构化 wiki 文章。

### 4. 查询知识库

```
/kb query "你的问题"
```

生成结构化报告，包含分析、结论和回填建议。

### 5. 回填有价值的结果

```
/kb file
```

将查询报告中有价值的内容并入 wiki。

### 6. 健康检查

```
/kb lint
```

六项检查：断链、孤岛、溯源、一致性、覆盖度、空白发现。

### 7. 查看状态

```
/kb status
```

仪表盘展示整体健康度和统计信息。

---

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

## 支持的文件格式

| 格式 | 后缀 | 说明 |
|------|------|------|
| PDF | .pdf | 提取文本和图片 |
| Excel | .xlsx, .xls, .csv | 提取表格内容 |
| 图片 | .png, .jpg, .jpeg | OCR 文字识别 |
| Word | .docx | 提取段落和表格 |

---

## 工作流程

```
投喂原料          LLM 编译          查询使用
    │                │                │
    ▼                ▼                ▼
 raw/ ──────► wiki/ ──────► 查询分析 ──────► 回填
    │                │                │
 原始文件        结构化文章       知识增长
```

---

## 目录结构

```
{知识库根目录}/
├── raw/                    # 原始资料（只读）
│   └── .extracted/        # 提取的文本（自动生成）
├── wiki/
│   ├── concepts/          # 核心概念
│   ├── sources/           # 来源摘要
│   └── comparisons/       # 对比分析
├── output/
│   ├── analysis/          # 查询报告
│   └── slides/           # 幻灯片
├── index/
│   ├── MASTER-INDEX.md   # 全局索引
│   ├── TOPIC-MAP.md      # 主题分组
│   ├── RAW-REGISTRY.md   # 原始文件登记
│   ├── LINT-REPORT.md    # 健康检查报告
│   └── ONTOLOGY.md       # 本体定义
└── scripts/
    ├── ingest.py          # 预处理脚本
    └── extractors/        # 文件提取器
```

---

## Python 依赖

首次使用需要安装依赖：

```bash
pip install -r .claude/skills/kb/scripts/requirements.txt
```

依赖列表：
- PyMuPDF — PDF 提取
- openpyxl — Excel 读取
- pandas — 数据处理
- pytesseract — 图片 OCR
- python-docx — Word 读取
- Pillow — 图片处理

---

## SessionStart Hook（可选）

配置后，每次打开 Claude Code 会自动检测 `raw/` 中的新文件并提醒处理。

初始化时选择"是"即可启用。
