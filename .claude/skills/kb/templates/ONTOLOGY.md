# Ontology

## 实体类型

| 类型 | 目录 | 命名规则 | 说明 |
|------|------|---------|------|
| concept | wiki/concepts/ | {slug}.md | 核心概念 |
| source | wiki/sources/ | {slug}.md | 来源摘要 |
| comparison | wiki/comparisons/ | {a}-vs-{b}.md | 对比分析 |

## 关系

- 用 `[[双链]]` 表达引用关系
- frontmatter 的 `compiled_from` 表达溯源
- frontmatter 的 `related` 表达关联

## Wiki 文章模板

每篇 wiki 文章使用以下结构：

```yaml
---
type: {entity_type}
id: {slug}
aliases: []
compiled_from:
  - raw/{source_file}
related:
  - "[[other-article]]"
last_compiled: {date}
---
```

### 正文结构

```markdown
# {标题}

## 概述
一段话定义...

## 要点
- ...

## 关联
- [[相关概念]]

## 来源
- 编译自 raw/xxx.pdf
```
