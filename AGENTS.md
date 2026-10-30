# Agent 开发：项目约定

本目录存放自研 agent 项目，并维护通用开发规范。**在这里新建 agent 时，先读 `docs/01-流程规范.md`。**

## 目录分工

- `docs/`：通用规范（流程、分层、形态、评测、发布、反模式）。跨项目共用，不要往这里塞单个项目的细节。
- `templates/`：需求卡、设计、契约、ADR、发布说明；`project-skeleton/` 是可复制的骨架。
- `checklists/`：四个阶段的可勾选清单。
- `scripts/`：新建项目、跑评测、结构自检。
- `<agent-name>/`：每个 agent 一个独立子目录，自带 README、契约、评测。

## 新建一个 agent

```bash
./scripts/new-agent.sh <kebab-case-name>
cd <name> && make run && make evals
```

骨架自带 3 条 smoke 用例与一个规则占位实现，只用于验证链路；真实实现替换 `src/agent.py`，保持 stdin/stdout 契约不变。

## 硬性约定（所有 agent 通用）

1. 先有 `docs/contract.md`，再写实现。契约变了就是主版本变化。
2. 输入从 stdin、结果从 stdout（JSON），失败也输出 JSON 并返回非零退出码。
3. 失败必须显式：有 `error.code`、`message`、`hint`；禁止 `except: pass`。
4. 提示词与代码分开存放；提示词或模型变更必须重跑评测并写 CHANGELOG。
5. 密钥走环境变量，`.env` 不入库。
6. 评测用例 ≥30 条、含负例、有基线；`make evals` 一条命令可跑；查回退时加 `--report` 留快照。
7. 提交前跑 `make test && make evals && make check`。
8. 需要外部数据时，先建 `data/catalog.json` 清册与 `data/sources/<id>.md` 逐源说明；原始数据不入库，规则见 `docs/07-数据与知识接入.md`。

## 命名

项目目录 kebab-case；工具名 `动词_名词`；用例 id `类别-序号`；版本语义化。代码、字段、错误码用英文，文档与注释用中文。

## 中文排版

中文内容使用弯引号（U+201C/U+201D、U+2018/U+2019），不使用 ASCII 直引号。`scripts/check-structure.py` 校验配对，并在中文正文里用了直引号时给提醒（代码块与行内代码不算）。
