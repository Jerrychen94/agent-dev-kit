# Agent 开发规范套件

一套**跨形态通用**的 agent 开发流程规范、模板与检查清单。适用形态：提示词工作流（Skill）、MCP Server、独立 LLM 应用、多 agent 编排。

设计取舍：形态会变，流程不变。所以规范只规定“必须回答哪些问题、必须有哪些产出、什么算做完”，具体技术栈由项目自选。

零依赖：只用 Python 标准库与 bash，三个脚本拷走即可独立使用。

## 30 秒上手

```bash
git clone https://github.com/Jerrychen94/agent-dev-kit.git
cd agent-dev-kit

# 新建一个 agent 项目（生成在套件根目录下，与 docs/ templates/ 平级）
./scripts/new-agent.sh my-agent-name

# 进项目，跑通最小链路与评测
cd my-agent-name
make run     # 走一遍示例链路
make evals   # 跑评测用例
```

生成出来的是独立项目，不要混进本仓库的提交里；要长期维护就单独建仓（骨架自带 `.gitignore`）。

## 目录地图

| 路径 | 内容 |
|---|---|
| [docs/01-流程规范.md](docs/01-流程规范.md) | 六阶段流程与退出门禁（**先读这份**） |
| [docs/02-分层模型与项目结构.md](docs/02-分层模型与项目结构.md) | 六层模型、标准目录、命名与版本约定 |
| [docs/03-形态适配指南.md](docs/03-形态适配指南.md) | Skill / MCP / 应用 / 多 agent 各自的骨架与坑 |
| [docs/04-评测与质量规范.md](docs/04-评测与质量规范.md) | 用例格式、指标、判分、回归 |
| [docs/05-发布运维与安全.md](docs/05-发布运维与安全.md) | 密钥、成本、日志、危险操作、回滚 |
| [docs/06-反模式与速查.md](docs/06-反模式与速查.md) | 十条反模式、写法对照、决策速查 |
| [docs/07-数据与知识接入.md](docs/07-数据与知识接入.md) | 数据放哪、多源清册、连接器与合规 |
| [templates/](templates/) | 需求卡、设计文档、契约、ADR、发布说明、数据源清册与说明模板 |
| [templates/project-skeleton/](templates/project-skeleton/) | 可直接复制的项目骨架（自带最小 agent + 3 条用例） |
| [checklists/](checklists/) | 立项 / 开发 / 上线 / 复盘 四份可勾选清单 |
| [scripts/](scripts/) | 新建项目、跑评测、结构自检 |
| [AGENTS.md](AGENTS.md) | 本目录的项目约定（编码 agent 自动加载） |

## 用这套件做出来的项目

| 项目 | 说明 | 状态 |
|---|---|---|
| [ppt-agent](https://github.com/Jerrychen94/ppt-agent) | 从 brief 生成可编辑 PPTX：9 种版式、4 套主题、确定性溢出检查、HTML 预览与讲稿 | v0.1.0，评测 37/37 |

另有几个不公开的项目（经济金融论文写作、金融研究）按同一套流程维护。新项目一律平级新建、互不依赖；项目内部约定写各自的 `AGENTS.md`。

## 六阶段与门禁

| 阶段 | 一句话 | 门禁 |
|---|---|---|
| 0 立项 | 说清给谁解决什么问题 | 一句话说清输入→输出 + 5 条真实样例 + 可量化判据 |
| 1 设计 | 定边界与契约 | 工具每个有真实用例；写明不做什么；评测方案定了 |
| 2 最小链路 | 端到端跑通 | 一条命令可复现；有结构化日志；失败显式 |
| 3 评测打磨 | 用数据变好 | ≥30 条用例；达标；负例不崩；两次稳定 |
| 4 上线 | 安全地跑 | 清单全绿；可回滚；有成本上限 |
| 5 复盘 | 不重复踩坑 | 失败入库；有下一轮假设 |

阶段 3 应占一半以上时间。文档细节见 [docs/01-流程规范.md](docs/01-流程规范.md)。

## 三种使用方式

**新建项目**：复制骨架 → 填 [需求卡](templates/需求卡.md) → 写 [契约](templates/契约.md) → 跑通链路 → 建评测。按 [checklists/01-立项清单](checklists/01-立项清单.md) 往下走。

**接手/改造已有 agent**：先补 `docs/contract.md`（它缺什么一目了然），再补评测，再看安全项。不要先改代码。

**准备上线**：只做两件事——逐条过 [上线清单](checklists/03-上线清单.md)，跑一次全量评测并留基线。

## 配套工具

```bash
./scripts/new-agent.sh <name>              # 从骨架新建项目
python3 scripts/run-evals.py <project-dir> # 跑评测（含基线对比）
python3 scripts/check-structure.py <project-dir>  # 检查项目是否满足规范
```

## 自检口径

规范自己也要能被检查：`python3 scripts/check-structure.py .` 会校验本套件的文档链接与关键文件是否齐全。

## 维护约定

- 规范随实践更新：踩过的坑写进 [docs/06-反模式与速查.md](docs/06-反模式与速查.md)，不要另开碎文档。
- 新增模板放在 `templates/`，新增可复用脚本放在 `scripts/`，并在本文件登记。
- 项目专属约定写到各项目自己的 `README.md` 或 `AGENTS.md`，不要污染本目录的通用规范。

## 许可证

MIT，见 [LICENSE](LICENSE)。拿去用、改、商用都可以，保留版权声明即可。
