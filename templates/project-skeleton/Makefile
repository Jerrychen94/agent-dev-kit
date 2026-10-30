TOOLS ?= ../scripts

.PHONY: help run evals smoke test check

help:
	@echo "make run    跑一条示例输入"
	@echo "make evals  跑全部评测用例"
	@echo "make smoke  只跑 smoke 用例"
	@echo "make test   单元测试"
	@echo "make check  结构自检（需 ../scripts/check-structure.py）"

run:
	@echo "2026年3月5日发票，金额 1,280.50 元，开票方：示例科技" | python3 src/agent.py

evals:
	python3 $(TOOLS)/run-evals.py .

smoke:
	python3 $(TOOLS)/run-evals.py . --tag smoke

test:
	python3 -m unittest discover -s tests -v

check:
	python3 $(TOOLS)/check-structure.py .
