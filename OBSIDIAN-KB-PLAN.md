# Hello-Agents Obsidian 知识库改造计划

> 参考架构：`D:\privategit\github\ai-agent-book`
> 目标：把本仓库改造为同款 Obsidian 项目知识库。本文件是施工图，执行时按 Phase 顺序推进。

---

## 1. 参考架构（ai-agent-book 模式提炼）

| 要素 | 做法 |
|---|---|
| Vault 位置 | 仓库根 = vault 根；知识库集中在 `kb/` 子目录，不搬动原有内容 |
| 隔离噪音 | `.obsidian/app.json` 的 `userIgnoreFilters`（正则）把翻译镜像、归档对话、工程产物挡在 Obsidian 搜索/快速切换之外（链接仍有效） |
| 链接方式 | 最短路径 `[[wikilink]]`（`useMarkdownLinks: false`、`newLinkFormat: "shortest"`、`alwaysUpdateLinks: true`）；非 md 文件用相对 markdown 链接 |
| 导航层 | `HOME.md`（入口）→ `MOC - xxx 知识体系.md`（总目录，按篇章分组、难度星级）→ `📋 看板.md`（Dataview 仪表盘）+ `项目地图.md` + `工程手册.md` + `📅 学习计划.md` |
| 笔记三类 | `章节/`（每章一页导读，链接正文+配套实验）、`概念/`（手写知识卡片，含闪卡）、`实验/`（脚本生成的代码索引卡）；另有 `实验拆解/`（用户动手笔记，Templater folder-template 自动套模板） |
| 元数据驱动 | frontmatter：`type`（章节/概念/实验/拆解/MOC…）、`status`、`chapter`、`category`、`difficulty`、`review_dates`、`tags`；Dataview 看板和 `.base` 视图全部由 frontmatter 驱动 |
| 标签体系 | `ai-agent/<篇章>`（基础/上下文/工具/评估与进化/拓展协作），用于图谱分色和闪卡分组 |
| 可视化 | `全书知识地图.canvas`（篇章分色 group + 关系边）+ `实验看板.base`（filters/formulas/多视图）+ CSS snippet 按目录着色 |
| 插件 | dataview、templater-obsidian、obsidian-spaced-repetition、omnisearch（共 4 个） |
| 索引生成 | `scripts/gen_kb_index.py` 幂等生成实验索引笔记，解析各章 README 的实验表格 |

## 2. 现状盘点（Hello-Agents 关键事实）

- **无 `.obsidian`**，全新建库。仓库是 docsify 站点（`docs/index.html` + `_sidebar.md`），改造是**纯增量**，不影响线上站点。
- 正文：`docs/chapter1~16/`，每章中文 md（文件名含空格，如 `第一章 初识智能体.md`）+ 英文镜像（`ChapterN-*.md`）；图片 210 张，正文里用 GitHub raw 绝对 URL（Obsidian 可直接渲染，**无需改写**）。
- 代码：`code/chapter1~16`（156 py + 29 md + 1 ipynb；ch13-15 是完整工程项目；ch16 仅一份共创路径说明）；`code/learn/` 是**个人练习区**（w1_*、w2_* 共 12 个 py，对应 4 周计划）。
- 个人文档（根目录）：`STUDY-PLAN-4WEEKS.md`（4 周速通）、`LEARNING-PLAN.md`（29 周长线）、`PITFALLS-GUIDE.md`（1414 行避坑指南，十篇）、`ENV-REPORT.md`。
- 社区内容：`Extra-Chapter/`（15 篇扩展文章）、`Co-creation-projects/`（37 个项目，126 md + 18 ipynb，噪音大，应折叠进 MOC 而非逐篇入 kb）。
- 现有链接全部是相对 md 链接 / 绝对 URL，无 wikilink——kb 全部新建，不碰旧文件。

## 3. 目标结构

```
kb/
├── HOME.md                        入口导读（含库结构树、30 秒上手）
├── MOC - Hello-Agents 知识体系.md  总目录（按五部分分组 + 难度星级）
├── 📋 学习看板.md                  Dataview 仪表盘（进度/状态/拆解统计）
├── 📅 学习计划.md                  串起 4 周速通 + 29 周长线两个计划
├── 项目地图.md                     仓库各区域速览（含 Co-creation 折叠 MOC）
├── 工程手册.md                     环境/运行/维护速查（conda、docsify、gen_kb_index）
├── 全书知识地图.canvas             五部分分色 + 阅读主线边
├── 实验看板.base                   code/ 实验的数据库视图
├── _Templates/                    Templater 模板（见 §6）
├── 章节/  ×16                     第01章 · 初识智能体.md …（零填充编号）
├── 概念/                          手写知识卡片（见 §3.1 清单）
├── 实验/  ~40                     脚本生成的代码索引卡
├── 练习拆解/                      个人动手笔记（code/learn 的 w1_*/w2_*）
└── assets/                        附件落地目录（attachmentFolderPath）
```

**命名约定**（沿用参考库）：章节 `第NN章 · 标题`；实验 `实验 N-序号 · 名称`；模板前缀 `tp-`；仪表盘 emoji 前缀；frontmatter `type` 字段区分笔记类型。

### 3.1 概念笔记初始清单（种子，手写层）

两路来源：
1. 正文核心概念：智能体定义、ReAct、Plan-and-Solve、Reflection、低代码平台（Coze/Dify/n8n）、多智能体框架（AutoGen/CAMEL/AgentScope/LangGraph）、记忆、RAG、多智能体协作、MCP、评估、LoRA 微调、GRPO 训练……
2. `PITFALLS-GUIDE.md` 十篇主题 → 避坑概念卡：Agent≠Chatbot、工具调用≠函数调用、Token 计量、可变默认参数、`==` vs `is`、作用域与闭包、ABC/MRO/鸭子类型、venv 与 `pip -e`、流式与 Function Calling、async/await 心智模型、LoRA 显存账、GRPO vs PPO。

不必一次写完：先建 6-8 张最核心的（ReAct、记忆、RAG、MCP、Agent≠Chatbot、Token、LoRA、多智能体），其余随学习进度用 `tp-概念笔记` 增补。

### 3.2 标签体系（图谱分色 + 闪卡分组）

`ha/<篇章>`，对应 README 五部分（执行时以 README 导航表为准核对章节归属）：

| 标签 | 篇章 | 章节（待核对） |
|---|---|---|
| `ha/基础` | 第一部分 | ch1-3 |
| `ha/构建` | 第二部分 | ch4-7 |
| `ha/高级` | 第三部分 | ch8-12 |
| `ha/综合案例` | 第四部分 | ch13-15 |
| `ha/毕业设计` | 第五部分 | ch16 |
| `ha/避坑` | PITFALLS-GUIDE 派生 | — |

闪卡标签 `#flashcards/ha/<篇章>`，与上表同构。

### 3.3 统一 frontmatter schema

```yaml
---
title:
aliases: []
type: 章节 | 概念 | 实验 | 项目 | 练习拆解 | MOC | 看板 | 导读
chapter: 4            # 章节/实验/项目笔记必填
status: 未开始 | 进行中 | 已完成   # 驱动看板
category: 范式        # 概念笔记的分类
difficulty: ⭐~⭐⭐⭐⭐⭐
review_dates: []      # 间隔复习
created: YYYY-MM-DD
tags: [ha/构建]
---
```

## 4. 分阶段实施计划

### Phase 0 · 前置（10 min）
- [ ] 当前分支 `dev_001101` 上有未提交内容（w2_*、PITFALLS、STUDY-PLAN 等）——先单独提交，再开新分支 `feat/obsidian-kb`。
- [ ] `.gitignore` 追加：`.obsidian/workspace.json`、`.obsidian/workspace-mobile.json`、`__pycache__/`（已有则跳过）。

**验收**：工作区干净，新分支就绪。

### Phase 1 · Vault 初始化（30 min）
- [ ] 建 `.obsidian/`：`app.json`（`useMarkdownLinks:false`、`newLinkFormat:"shortest"`、`alwaysUpdateLinks:true`、`attachmentFolderPath:"kb/assets"`、`showUnsupportedFiles:false`、`userIgnoreFilters`）。
- [ ] `userIgnoreFilters` 初版正则（目标：中文正文和 kb 可见，其余降噪）：
  - 英文镜像：`docs/chapter\d+/Chapter\d+-.*\.md`、`README_EN\.md`、`docs/_sidebar_en\.md`
  - 噪音目录：`^\.zcode/`、`^\.github/`、`^\.vscode/`、`__pycache__`、`node_modules`
  - 共创项目内部：`^Co-creation-projects/(?!README)[^/]+/`（只留总 README 入口，项目笔记由 MOC 链接承载）
  - docsify 杂项：`docs/index\.html`
- [ ] `core-plugins.json`（file-explorer、graph、backlink、canvas、properties、daily-notes、bookmarks、outline、bases=true）；`graph.json` 按 §3.2 标签分色。
- [ ] 安装 4 个社区插件（dataview、templater-obsidian、obsidian-spaced-repetition、omnisearch）并写入 `community-plugins.json`；Templater 配置 `templates_folder: "kb/_Templates"` + folder templates（`kb/概念 → tp-概念笔记`、`kb/练习拆解 → tp-练习拆解`）。
- [ ] `snippets/kb-colors.css`：按 kb 子目录着色（参照参考库改标签名）。
- [ ] 用 obsidian CLI 把仓库注册/打开为 vault（`obsidian://open?path=...` 首次挂载，后续 `obsidian vault="Hello-Agents" ...`）。

**验收**：`obsidian vault="Hello-Agents" read file="HOME"` 之类命令可通；`obsidian dev:errors` 无报错。

### Phase 2 · 导航层（1 h）
- [ ] `kb/HOME.md`：frontmatter + callout 简介 + 入口表格 + ASCII 库结构树 + `![[实验看板.base]]` 嵌入 + 三份个人计划文档入口。
- [ ] `kb/MOC - Hello-Agents 知识体系.md`：五部分分组列 16 章链接 + 难度星级 + 配套实验/概念交叉链接。
- [ ] `kb/项目地图.md`：docs（正文）/code（实验）/Extra-Chapter（扩展）/Co-creation（共创，折叠列表）/根文档（三份个人计划）。
- [ ] `kb/工程手册.md`：conda 环境、各章代码运行方式、`python scripts/gen_kb_index.py` 维护说明、docsify 本地预览。
- [ ] `kb/📅 学习计划.md`：4 周速通（Day 粒度链接到章节/练习拆解）+ 29 周长线（周粒度）。

**验收**：从 HOME 出发 3 跳内可达任意章节/实验/计划。

### Phase 3 · 章节笔记 ×16（脚本辅助 + 手工校对，2 h）
- [ ] 每章一页 `kb/章节/第NN章 · 标题.md`：`> [!abstract]` 一句话摘要 + 小节列表 + 阅读入口 `[[docs/chapterN/第一章 xxx|正文]]` + 配套代码表格（表内 `\|` 转义）+ 相关 Extra-Chapter 文章 + 上/下一章导航 + 3-5 张闪卡。
- [ ] 章名/摘要/小节从各章 md 的标题行脚本提取生成骨架，人工补摘要与闪卡。

**验收**：16 页齐全，frontmatter 完整，正文 wikilink 全部可解析（`obsidian backlinks` 抽查）。

### Phase 4 · 实验索引生成器（2 h）
- [ ] 写 `scripts/gen_kb_index.py`（参照 ai-agent-book，适配本仓库）：
  - 输入：`code/chapter*/` 目录树 + `scripts/kb_manifest.yaml`（手写映射：每个实验的编号、名称、一句话说明、icon ✅/📖/🚧）
  - 输出：`kb/实验/实验 N-序号 · slug.md`，frontmatter（chapter/code/codes/type/icon/status/tags）+ 5 条标准链接（归属章节、正文、源码文件、相关概念）；幂等可重跑，生成尾部打 `<!-- generated by scripts/gen_kb_index.py -->`
  - ch13-15 完整工程 → 生成 `kb/实验/项目 N · xxx.md`（type: 项目）；ch5 低代码导出文件按材料链接处理
- [ ] 首跑 `python scripts/gen_kb_index.py` 生成约 40 张实验卡，人工抽查 10%。

**验收**：重跑无 diff（幂等）；`实验看板.base` 能按章/类型分组展示。

### Phase 5 · 概念笔记种子（8 张，1.5 h）
- [ ] 按 §3.1 首批清单写 8 张：ReAct、记忆、RAG、MCP、Agent≠Chatbot、Token 计量、LoRA、多智能体协作。
- [ ] 结构复刻参考库：是什么 / 为什么重要 / 在书中的位置（表格）/ 相关概念 / 🃏 闪卡（`#flashcards/ha/<篇章>` + `问？::答`）。

**验收**：每张卡有 ≥3 个 wikilink；spaced-repetition 插件能识别卡组。

### Phase 6 · 个人练习层（45 min）
- [ ] `kb/练习拆解/` + `.gitkeep`；Templater folder-template 就位。
- [ ] 为 `code/learn/w1_01` ~ `w2_07` 建 12 张拆解卡骨架（目标→运行观察→对照验收→沉淀），链接对应 py 文件与 STUDY-PLAN 的 Day 条目。
- [ ] `kb/📋 学习看板.md`：Dataview 汇总（章节进度、实验状态、拆解统计、待复习闪卡数）。

**验收**：在 `kb/练习拆解/` 新建文件自动套模板；看板表格出数。

### Phase 7 · Canvas + Base + 收尾（1 h）
- [ ] `kb/全书知识地图.canvas`：五部分 group 分色 + 16 章节 file 节点 + 主线边（阅读主线/配套实验）。
- [ ] `kb/实验看板.base`：filters（`file.inFolder("kb/实验")`）+ formulas（badge）+ 3 视图（按章表/按类型表/卡片）。
- [ ] 图谱分色核对；CSS snippet 生效。

**验收**：`obsidian dev:screenshot` 或人工目检 canvas/base 渲染正常。

### Phase 8 · 验证与提交（30 min）
- [ ] 全库 wikilink 解析检查（脚本扫描 `[[...]]` 目标存在性）。
- [ ] `obsidian dev:errors` 清零；抽查 backlinks。
- [ ] `.gitignore` 复核（workspace.json 不入库，插件目录入库存疑则跟随参考库一并提交）。
- [ ] 分两个 commit：`feat: init obsidian vault (kb navigation layer)` + `feat: add kb content (chapters/experiments/concepts)`，发起 PR 到 main。

## 5. 风险与对策

| 风险 | 对策 |
|---|---|
| 中文+空格文件名的 wikilink | Obsidian 原生支持（`[[第一章 初识智能体]]`），但旧文档里的 `%20` 相对链接不动它们即可——kb 全部新建 wikilink |
| `userIgnoreFilters` 正则误伤 | 只隐藏"英文镜像/工程噪音/共创项目内部"，隐藏后链接仍可解析；逐条验证 |
| 共创项目 126 md 拖慢索引 | 靠 ignore filters 排除 + 项目地图只留总入口 |
| docsify 站点回归 | kb 是纯增量目录，`docs/`、`_sidebar.md`、`index.html` 一律不改 |
| 社区插件版本漂移 | `community-plugins.json` + 插件目录入 git，保证克隆即用 |
| 大仓库首开索引慢 | omnisearch 首次建索引慢属正常；ignore filters 已显著缩小范围 |

## 6. 模板清单（`kb/_Templates/`）

- `tp-概念笔记.md`：suggester 选篇章/难度 → frontmatter + 是什么/为什么/书中位置/相关概念/闪卡骨架
- `tp-练习拆解.md`：suggester 选周次/练习 → frontmatter + 目标→运行观察→对照验收→沉淀 + 闪卡占位

## 7. 总量预估

kb/ 首版约 **90-100 个 md**（导航 7 + 章节 16 + 实验/项目 ~40 + 概念 8 + 拆解 12 + 模板 2 + base/canvas 各 1）+ `scripts/gen_kb_index.py` + `scripts/kb_manifest.yaml`。纯增量，不动现有 217 个 md。
