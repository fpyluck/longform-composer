# Longform Composer — 大型 Markdown 交付物编排技能
# Longform Composer — Large Markdown Deliverable Orchestration Skill

> 不要把大型交付物塞进一条聊天消息。把长文工作转化为持久化 Markdown 制品、显式检查点、确定性验证和最终合并交付物。

---

## What's New — 2026-05-30

- **新增 `scripts/export_longform.py`**：将合并后的 Markdown 导出为 `exports/*.docx` 及其他支持格式，完整保留内容，不做摘要压缩。
- **更新 `scripts/longform_common.py`**：共享工具函数和路径约定更新。
- **更新 `scripts/merge_markdown.py`**：合并逻辑改进，章节边界处理更稳健。
- **更新 `scripts/init_longform_project.py`**：项目脚手架初始化更新。
- **更新 `scripts/self_test.py`**：冒烟测试覆盖新增的 export 脚本。
- **更新 `scripts/validate_longform.py`**：验证逻辑与新 schema 字段对齐。
- **更新 `references/operating-protocol.md`**：操作协议更新，反映 export 路由。
- **更新 `references/quality-gates.md`**：质量门控更新。
- **更新 `references/manifest-schema.md`**：manifest schema 文档更新。
- **更新模板 `assets/templates/index.md`**：包含更多字段。
- **更新模板 `assets/templates/manifest.yaml`**：包含更多字段。

---

## 是什么

Longform Composer 是一个 Claude Code / Codex / Gemini 三端技能，用于生产超出单条聊天响应容量的综合 Markdown 交付物。它规划工作、创建 manifest、写入章节文件、验证进度，并合并最终 Markdown。

**这个技能是打包和工作流层**：它保留模型的预期含义、主张、强调、不确定性和面向用户的答案语义，只改变组织、存储和交付方式。

---

## 触发条件

以下情况触发 Longform Composer：

- 用户要求完整的、系统性的教程、报告、手册、白皮书、评审、规范、书籍式回答
- 用户要求分段 Markdown 文件、章节、续接锚点、manifest、检查点或最终合并 Markdown
- 用户说输出太短或被截断
- 任务可能需要多个章节、文件、示例或多轮处理
- 文件系统不可用时，显式请求仅聊天输出

---

## 包含资源

### 核心
- `SKILL.md` — 主技能指令和触发描述

### References
- `references/operating-protocol.md` — 操作协议
- `references/quality-gates.md` — 质量门控
- `references/manifest-schema.md` — manifest schema 文档
- `references/chat-only-protocol.md` — 仅聊天模式协议
- `references/examples.md` — 示例和模式

### Templates
- `assets/templates/manifest.yaml` — manifest 模板（含更多字段）
- `assets/templates/index.md` — 索引模板（含更多字段）
- `assets/templates/chapter.md` — 章节模板

### Scripts
- `scripts/init_longform_project.py` — 创建项目脚手架
- `scripts/validate_longform.py` — 验证项目状态和章节文件
- `scripts/merge_markdown.py` — 合并章节为 `final/final_merged.md`
- `scripts/export_longform.py` — 导出合并 Markdown 为 DOCX/PDF 等格式，不做摘要
- `scripts/split_markdown.py` — 将现有 Markdown 文件拆分为章节文件
- `scripts/longform_common.py` — 共享工具函数
- `scripts/self_test.py` — 冒烟测试

`init_longform_project.py --force` 刷新生成文件但保留已编写的章节内容。仅在有意替换现有章节文件时使用 `--overwrite-chapters`。

---

## 项目结构

```
long_output/<project-slug>/
  manifest.yaml          # 项目元数据和章节列表
  index.md               # 目录和导航
  chapters/
    01_*.md
    02_*.md
    ...
  final/
    final_merged.md      # 最终合并交付物
  exports/
    *.docx               # export_longform.py 输出
```

---

## 安装

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

三端（claude/、codex/、gemini/）均支持，通过各自的 agent 配置加载。

---

## 快速测试

```bash
python scripts/self_test.py
```
