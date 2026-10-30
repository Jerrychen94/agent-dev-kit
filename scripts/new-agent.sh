#!/usr/bin/env bash
# 从骨架新建一个 agent 项目。
# 用法: ./scripts/new-agent.sh <kebab-case-name>
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKELETON="$ROOT/templates/project-skeleton"
NAME="${1:-}"

if [[ -z "$NAME" ]]; then
  echo "用法: $0 <项目名>  （kebab-case，例如 invoice-reconciler）" >&2
  exit 1
fi

if [[ ! "$NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "项目名只能用小写字母、数字、连字符，且以字母或数字开头: $NAME" >&2
  exit 1
fi

TARGET="$ROOT/$NAME"
if [[ -e "$TARGET" ]]; then
  echo "目标已存在: $TARGET" >&2
  exit 1
fi

cp -R "$SKELETON" "$TARGET"
rm -f "$TARGET/evals/baseline.json"

python3 - "$TARGET" "$NAME" <<'PY'
import sys
from pathlib import Path

target = Path(sys.argv[1])
name = sys.argv[2]
for path in target.rglob("*"):
    if path.is_file() and path.suffix in {".md", ".json", ".py", ".Makefile", ".example", ""}:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new = text.replace("<agent-name>", name).replace("invoice-field-extractor", name)
        if new != text:
            path.write_text(new, encoding="utf-8")
PY

cat <<EOF

已创建: $TARGET

接下来（按顺序）：
  1. 填 docs/../需求卡 → 先想清楚给谁解决什么问题
  2. 改 docs/design.md 与 docs/contract.md（骨架里是发票抽取示例，按需替换）
  3. 替换 src/agent.py 为真实实现，保持 stdin/stdout 契约
  4. cd $NAME && make run && make evals
  5. 评测达标后: python3 ../scripts/run-evals.py . --update-baseline

注意：骨架自带 3 条 smoke 用例与规则占位实现，仅用于验证链路是否通。
EOF
