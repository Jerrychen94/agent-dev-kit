# 变更记录

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号用语义化版本。

## v1.1.0 — 2026-10-31

### 新增

- `run-evals.py --report`：把一次评测落成快照 `evals/runs/<时间>.json`，含每条用例的输入、stdout、stderr、耗时、退出码与失败原因（单字段超长自动截断）；下次运行自动与上次对比，直接列出“哪几条由通过转失败”；带 `--tag` 的快照不与全量快照互相比。快照只留本地，基线仍由 `--update-baseline` 管。
- 基线多记一个 `failed` 名单，打开 `baseline.json` 就能看到上一轮挂在哪几条。
- `.github/workflows/ci.yml`：CI 跑套件自检，并从骨架生成一个临时项目，跑单测、评测、结构自检与快照，验证“拷走就能用”这件事没坏。
- `check-structure.py` 新增中文直引号提醒：代码块与行内代码之外的正文里出现 ASCII 直引号时给出提醒，并顺手修掉 `docs/07` 里原有的两处。

### 修正

- `check-structure.py` 的套件自检漏了 `docs/07-数据与知识接入.md`、`templates/数据源说明.md`、`templates/data-catalog.json`，删掉这几份也照样“通过”；已补上。
- `check-structure.py` 对项目不再只看文件在不在：`evals/config.json` 缺 `cmd` 直接阻断；`evals/runs/` 有快照却没被 `.gitignore` 忽略时给提醒。
- 骨架 `.gitignore` 里的 `evals/report-*.json` 对应一条从未存在的约定，改为忽略 `evals/runs/`。
- 骨架 `Makefile` 调用工具脚本时没加引号，套件或项目路径含空格（例如放在 `Nutstore Files` 下）时 `make evals` 直接失败；已加引号。
- `new-agent.sh` 用 `pwd` 取路径，`/tmp` 这类符号链接目录下算出的相对路径会多一级，导致 `TOOLS` 指向不存在的文件；改用 `pwd -P`。
- `new-agent.sh` 结尾提示改用绝对路径并加引号，路径含空格时可整行复制。
- `docs/04-评测与质量规范.md` 增加第 6 节“运行快照”，原第 6、7 节顺延。

## v1.0.1 — 2026-10-31

### 修正

- 骨架 `AGENTS.md` 的上级规范路径写成 `../../docs/`，项目生成到套件根目录下时会指到套件外面；改为 `../docs/`。
- 骨架 ADR 里的规范引用少了相对前缀，改后能点到 `docs/03-形态适配指南.md`。
- `new-agent.sh` 结尾提示里的“填 docs/../需求卡”路径错误，改为套件内模板的真实位置。

### 新增

- `new-agent.sh` 支持 `--out <目录>`，可把项目建到套件外面；脚本按实际相对位置改写 `Makefile` 的 `TOOLS` 与文档里的上级规范路径，两种布局都能直接 `make evals`。

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
