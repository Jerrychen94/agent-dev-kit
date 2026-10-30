# 运行手册：invoice-field-extractor

## 启动

```bash
cd <项目目录>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt     # 如有
cp .env.example .env                # 填写 MODEL_API_KEY
make run
```

无外部依赖时可直接 `python3 src/agent.py`。

## 停止

CLI 进程随调用结束退出，无常驻服务。若改为服务形态，在此补充停止命令与端口。

## 常见故障

| 现象 | 可能原因 | 处理 |
|---|---|---|
| `EMPTY_INPUT` | 没传 stdin | 检查管道/调用方 |
| `NO_INVOICE` | 输入不含发票关键词 | 确认输入来源 |
| `UPSTREAM_TIMEOUT` | 模型超时 | 检查网络；重试 1–2 次 |
| `BUDGET_EXCEEDED` | 超过日成本上限 | 检查是否死循环；次日重置 |
| 输出非 JSON | 提示词被改坏 | 回滚 `prompts/system.md` |

## 日志

调试日志在 `<项目>/logs/`（如启用），行分隔 JSON，含 `trace_id`、`step`、`duration_ms`、`in_tokens`、`out_tokens`。

查找某次调用：

```bash
grep '"trace_id":"<id>"' logs/*.jsonl
```

## 回滚

```bash
git tag -l                       # 找上一个可用版本
git checkout <tag>               # 或 git revert <commit>
make evals                       # 跑 3 条 smoke 确认恢复
```

## 成本

单次约 <__> tokens，折合 <__> 元。预算见 `docs/contract.md` 第 7 节。
