# 变更记录

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号用语义化版本。

## v1.0.0 — 2026-10-31

首个公开版本：把原本与本机若干具体项目混放在一起的规范套件单独成仓，只保留可复用的通用部分。

### 新增

- `docs/` 七篇规范：六阶段流程与门禁、六层模型与项目结构、形态适配指南、评测与质量、发布运维与安全、反模式速查、数据与知识接入。
- `templates/` 需求卡、设计文档、契约、ADR、发布说明、数据源模板，以及可直接复制的 `project-skeleton/`（最小 agent + 3 条 smoke 用例 + 评测配置）。
- `checklists/` 立项、开发、上线、复盘四份可勾选清单。
- `scripts/` 三个脚本：`new-agent.sh` 从骨架建项目、`run-evals.py` 跑评测并对比基线、`check-structure.py` 做结构自检；只依赖 Python 标准库与 bash。
- `AGENTS.md`：给编码 agent 自动加载的硬性约定，和规范正文保持同源。

### 取舍

- 规范只规定“必须回答哪些问题、必须有哪些产出、什么算做完”，不绑定技术栈：Skill、MCP Server、独立 LLM 应用、多 agent 编排都适用。
- 示例项目不进本仓库，避免规范和实践互相带偏。
