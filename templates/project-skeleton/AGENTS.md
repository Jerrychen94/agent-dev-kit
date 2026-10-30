# 项目约定（给编码 agent）

上级通用规范：`../docs/`（流程、分层、评测、发布）。本文件只写本项目特有的约定，冲突时以本文件为准。

## 这是什么

<一句话：项目做什么。>

## 命令

```bash
make run      # 跑一条示例
make evals    # 全部评测
make smoke    # 只跑 smoke
make test     # 单元测试
make check    # 结构自检
```

## 结构约定

- 代码放 `src/`，提示词放 `prompts/`，两者分开。
- 评测用例放 `evals/cases/`，一条一个 JSON，`id` 唯一。
- 设计变更先改 `docs/`，再改代码。
- 输入输出契约以 `docs/contract.md` 为准；改契约必须升主版本并写 CHANGELOG。

## 编码约定

- 输出必须是 JSON，错误用 `{"ok": false, "error": {"code", "message", "hint"}}`。
- 不静默吞异常；不用 `except: pass`。
- 字段名与错误码只用英文，注释与文档用中文。
- 新增依赖要写进 README 与 requirements。
- 不提交 `.env`、密钥、真实客户数据。

## 改动后必须做

1. `make test` 与 `make evals` 都通过。
2. 改了提示词或模型 → 重跑全量评测，把指标写进 CHANGELOG。
3. 新增失败场景 → 加一条 eval 用例。
