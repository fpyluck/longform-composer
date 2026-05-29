<div align="center">

# 📄 Longform Composer

**长文写作技能 · AI 文档流水线**

*告别上下文截断，让 AI 真正写完一篇文档。*  
*Stop fighting context limits. Write documents that actually ship.*

[![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Gemini-5865F2?style=flat-square&logo=anthropic&logoColor=white)](https://github.com/anthropics/claude-code)
[![Type](https://img.shields.io/badge/type-superpowers%20skill-8B5CF6?style=flat-square)](.)
[![License](https://img.shields.io/badge/license-MIT-22C55E?style=flat-square)](LICENSE)
[![Maintained](https://img.shields.io/badge/maintained-yes-0EA5E9?style=flat-square)](.)

</div>

---

## 这是什么 · What It Is

Longform Composer 是一个用于 Claude Code、Codex 和 Gemini 的写作技能，将长文档生产变成一条有纪律的流水线：先规划清单，再分章写作，验证后合并，按需导出。

A writing skill for Claude Code, Codex, and Gemini that turns long-form document production into a disciplined pipeline — manifest first, chapters next, validate before merge, export on demand.

**这个技能是打包和工作流层**：它保留模型的预期含义、主张、强调、不确定性和面向用户的答案语义，只改变组织、存储和交付方式。

> This skill is a packaging and workflow layer: it preserves the model's intended meaning, claims, emphasis, uncertainty, and user-facing answer semantics — changing only organization, storage, and delivery.

---

## 为什么需要它 · The Problem

AI 很擅长写作，但不擅长写*长*。上下文窗口填满，响应被截断，一份一万字的技术报告变成了和模型注意力的拉锯战。

Longform Composer 把每份文档当作一个项目来管理：提前规划，独立成章，合并前验证，不丢失任何内容。

> AI assistants are great at writing. They're terrible at writing *long*. Context windows fill up, responses get cut short, and a 10,000-word technical report becomes a negotiation with the model's attention span. Longform Composer treats every document as a project: planned upfront, written in independent chapters, validated before merge, nothing lost.

---

## 核心功能 · Features

| | 功能 | Feature |
|---|---|---|
| 📋 | 写前规划清单，追踪每章状态 | Manifest-first planning with per-chapter status tracking |
| 📝 | 每章独立成文，不依赖对话历史 | Chapters written as independent files, no hidden chat dependency |
| ✅ | 合并前自动验证结构完整性 | Pre-merge validation: headings, placeholders, manifest consistency |
| 🔀 | 按清单顺序确定性合并，自动生成目录 | Deterministic merge in manifest order with generated TOC |
| 📤 | 导出 DOCX / PDF / PPTX，全文保留不压缩 | Export to DOCX / PDF / PPTX without summarizing or rewriting |
| 💬 | 无文件系统时自动切换分段对话续写模式 | Chat-only fallback with numbered parts and continuation anchors |

---

## 安装 · Installation

### Claude Code

```bash
claude skill install fpyluck/longform-composer
```

### Codex (OpenAI)

```bash
codex skill install fpyluck/longform-composer
```

### Gemini

```bash
gemini skill install fpyluck/longform-composer
```

---

## 快速开始 · Quick Start

```bash
# 1. 初始化项目 · Initialize a project
python scripts/init_longform_project.py \
  --title "My Technical Report" \
  --chapters "overview|background|implementation|results|conclusion"

# 2. 验证 · Validate
python scripts/validate_longform.py --root long_output/my-technical-report

# 3. 合并 · Merge
python scripts/merge_markdown.py --root long_output/my-technical-report

# 4. 导出 Word · Export to Word
python scripts/export_longform.py --root long_output/my-technical-report --format docx
```

```bash
# 冒烟测试 · Smoke test
python scripts/self_test.py
```

---

## 项目结构 · Project Layout

```
long_output/<project-slug>/
├── manifest.yaml        ← 权威状态与章节顺序 · authoritative state & chapter order
├── index.md             ← 目录与导读 · table of contents & reading guide
├── chapters/            ← 每章一个文件 · one file per chapter
│   ├── 01_overview.md
│   ├── 02_background.md
│   └── ...
├── final/
│   └── final_merged.md  ← 最终合并稿 · canonical merged deliverable
├── exports/             ← 生成的 DOCX / PDF / PPTX
├── logs/
│   └── progress.md      ← 变更日志 · change log
├── notes/               ← 草稿与备注
└── sources/             ← 参考资料
```

---

## 脚本说明 · Scripts

| 脚本 · Script | 用途 · Purpose |
|---|---|
| `init_longform_project.py` | 初始化项目脚手架（清单、目录、章节存根）· Scaffold manifest, index, chapter stubs |
| `validate_longform.py` | 验证清单一致性与合并就绪状态 · Check manifest, chapters, merge readiness |
| `merge_markdown.py` | 按清单顺序合并章节 · Merge chapters into `final/final_merged.md` |
| `export_longform.py` | 导出 DOCX / PDF / PPTX · Export to document formats |
| `split_markdown.py` | 将现有长文拆分为章节文件 · Split an existing long markdown into chapters |
| `longform_common.py` | 共享工具函数 · Shared utilities |
| `self_test.py` | 所有脚本冒烟测试 · Smoke test for all bundled scripts |

> `--force` 刷新生成文件但保留已写章节内容；`--overwrite-chapters` 才会覆盖章节。  
> `--force` refreshes generated files while preserving authored chapters. Use `--overwrite-chapters` only when intentional.

---

## 使用场景 · Use Cases

**技术白皮书与报告 · Technical white papers and reports**  
临床研究、工程规格、产品分析。清单保持结构诚实，验证在合并前捕获缺口。  
*Clinical research, engineering specs, product analyses. The manifest keeps structure honest; validation catches gaps before merge.*

**代码库文档 · Codebase documentation**  
当模型总是写得太少时，Longform Composer 将任务拆成章节逐一写完。若仓库有 `docs/` 目录，输出自动放入 `docs/longform/`。  
*When the model keeps writing too little, the skill breaks the task into chapters and writes each one completely.*

**拆分现有长文 · Splitting existing documents**  
用 `split_markdown.py` 将已有长 Markdown 拆成章节文件并自动生成清单。  
*Use `split_markdown.py` to break a long markdown file into chapter files and generate a manifest retroactively.*

**纯对话模式 · Chat-only mode**  
无文件系统时，技能自动宣告总段数，每次输出一段，并以续写锚点结尾。  
*When no filesystem is available, the skill announces total parts, outputs one at a time, and ends each response with a continuation anchor.*

---

## 参考资料 · Included Resources

| 路径 · Path | 说明 · Purpose |
|---|---|
| `SKILL.md` | Claude Code / Codex / Gemini 加载的主技能指令 · Main skill instructions |
| `references/operating-protocol.md` | 高风险大型交付物的详细工作流 · Detailed workflow for high-stakes deliverables |
| `references/manifest-schema.md` | 完整清单 Schema 与状态生命周期 · Full manifest schema and status lifecycle |
| `references/quality-gates.md` | 审查清单与失败处理 · Review checklist and failure handling |
| `references/chat-only-protocol.md` | 纯对话环境的续写协议 · Continuation protocol for chat-only environments |
| `references/examples.md` | 常见场景的注释示例 · Annotated examples for common use cases |
| `assets/templates/` | 可复用的清单、目录、章节模板 · Reusable manifest, index, and chapter templates |
| `agents/openai.yaml` | OpenAI Agents SDK / Codex 兼容配置 · Codex / OpenAI Agents SDK compatibility |

---

## 更新日志 · Changelog

### 2026-05-30
- 新增 `agents/openai.yaml`，支持 Codex / OpenAI Agents SDK · Added OpenAI Agents SDK compatibility
- `export_longform.py` 支持从章节摘要生成 PPTX · PPTX export derived from chapter summaries
- `init_longform_project.py --force` 默认保留已写章节；新增 `--overwrite-chapters` 标志 · `--force` now preserves authored chapters by default
- 合并前流程加入轻量「减法」审查，去除重复解释与低信号过渡 · Light subtraction pass added to pre-merge workflow
- `references/operating-protocol.md` 补充需求压缩与大纲设计指引 · Expanded with intake compression and outline design guidance
- 更新 `scripts/longform_common.py`、`merge_markdown.py`、`validate_longform.py` · Updated shared utilities and validation logic
- 更新模板 `assets/templates/manifest.yaml` 和 `index.md` · Updated templates with additional fields

### 2025 — 初始发布 · Initial Release
- 文件优先工作流：清单 → 章节 → 验证 → 合并 · File-first workflow
- 内置脚本套件：`init` / `validate` / `merge` / `export` / `split` / `self_test`
- 纯对话回退协议，支持分段续写 · Chat-only fallback with continuation anchors
- DOCX 导出（Pandoc 优先，`python-docx` 兜底）· DOCX export via Pandoc with python-docx fallback

---

<div align="center">

*Built for [Claude Code](https://github.com/anthropics/claude-code) · Part of the [superpowers](https://github.com/superpowers-sh/superpowers) skill ecosystem*

</div>
