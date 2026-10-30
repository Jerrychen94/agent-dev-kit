#!/usr/bin/env bash
# 从骨架新建一个 agent 项目。
# 用法: ./scripts/new-agent.sh [--out <目录>] <kebab-case-name>
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKELETON="$ROOT/templates/project-skeleton"
OUT="$ROOT"
NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)
      [[ $# -ge 2 ]] || { echo "--out 需要一个目录" >&2; exit 1; }
      OUT="$2"
      shift 2
      ;;
    -h|--help)
      sed -n '2,3p' "$0"
      exit 0
      ;;
    *)
      NAME="$1"
      shift
      ;;
  esac
done

if [[ -z "$NAME" ]]; then
  echo "用法: $0 [--out <目录>] <项目名>  （kebab-case，例如 invoice-reconciler）" >&2
  exit 1
fi

if [[ ! "$NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "项目名只能用小写字母、数字、连字符，且以字母或数字开头: $NAME" >&2
  exit 1
fi

mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
TARGET="$OUT/$NAME"
if [[ -e "$TARGET" ]]; then
  echo "目标已存在: $TARGET" >&2
  exit 1
fi

cp -R "$SKELETON" "$TARGET"
rm -f "$TARGET/evals/baseline.json"

python3 - "$TARGET" "$NAME" "$ROOT" <<'PY'
import os
import sys
from pathlib import Path

target = Path(sys.argv[1])
name = sys.argv[2]
root = Path(sys.argv[3])
rel = Path(os.path.relpath(root, target)).as_posix()


def rewrite(text: str) -> str:
    text = text.replace("<agent-name>", name).replace("invoice-field-extractor", name)
    # 项目不一定建在套件根目录下，按实际相对位置改写上级规范与工具的路径
    text = text.replace("../docs/", f"{rel}/docs/").replace("../scripts", f"{rel}/scripts")
    return text


for path in target.rglob("*"):
    if not path.is_file():
        continue
    if path.suffix in {".md", ".json", ".py", ".example", ""}:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new = rewrite(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
PY

REL="$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "$ROOT" "$TARGET")"

cat <<EOF

已创建: $TARGET

接下来（按顺序）：
  1. 填 $REL/templates/需求卡.md → 先想清楚给谁解决什么问题
  2. 改 docs/design.md 与 docs/contract.md（骨架里是发票抽取示例，按需替换）
  3. 替换 src/agent.py 为真实实现，保持 stdin/stdout 契约
  4. cd $TARGET && make run && make evals
  5. 评测达标后: python3 $REL/scripts/run-evals.py . --update-baseline

注意：骨架自带 3 条 smoke 用例与规则占位实现，仅用于验证链路是否通。
EOF
