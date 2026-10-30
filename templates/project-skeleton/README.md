# <agent-name>

> 一句话：当 <触发条件> 时，把 <输入> 变成 <输出>。

## 是什么

<两到三行：做什么、给谁用、不做什么。>

## 快速开始

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # 如有
cp .env.example .env              # 填入密钥
make run                          # 跑一条示例
make evals                        # 跑评测
```

依赖：<Python 版本、外部服务、模型 API>

## 用法

```bash
# CLI
echo "2026年3月5日发票，金额 1280.50 元，开票方：示例科技" | python3 src/agent.py

# JSON 输入
echo '{"text": "..."}' | python3 src/agent.py
```

输入输出契约见 [docs/contract.md](docs/contract.md)。

## 目录

| 路径 | 内容 |
|---|---|
| `src/` | 代码 |
| `prompts/` | 提示词（可版本对比） |
| `evals/` | 评测用例与配置 |
| `docs/` | 设计、契约、运行手册、决策记录 |
| `tests/` | 单元测试 |

## 评测

```bash
make evals                                    # 全部
make smoke                                    # 只跑 smoke 子集
python3 ../scripts/run-evals.py . --report    # 留一份运行快照到 evals/runs/（不入库）
python3 ../scripts/run-evals.py . --update-baseline   # 达标后更新基线
```

快照里存了每条用例的输入、输出与失败原因；下次运行会自动列出哪几条由通过转失败。

当前基线：<成功率 __%，更新于 __>

## 已知限制

- <限制 1>
- <限制 2>

## 变更记录

见 [CHANGELOG.md](CHANGELOG.md)。
