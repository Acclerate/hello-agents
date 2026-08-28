# Hello-Agents 一个月速通学习计划（4 周 / 28 天）

> **定制背景**：Java Web 7 年经验、886 工作制、GPU+CUDA 环境就绪、Python 语法学习中
> **核心策略**：用 Java 架构经验加速 60% 章节，集中火力攻克 Ch11 训练
> **每日时间**：工作日 1.5-2 小时（理论+代码），周末 5-6 小时（实战+项目）
> **每周总量**：约 15-18 小时 × 4 周 ≈ 65-70 总学时

> 📖 **配套文档**：[`PITFALLS-GUIDE.md`](./PITFALLS-GUIDE.md) — Java 后端/新手转 Agent 开发的避坑指南（10 篇，覆盖 Python/Agent/RAG/训练/异步的常见误解）。**学习每章前先读对应篇章**，遇到问题随时 `Ctrl+F` 查。

---

## 📊 已完成进度（不计入 4 周）

| 内容 | 状态 |
|------|------|
| conda 环境 `hello-agents` + torch+CUDA | ✅ |
| API Key 配置 + `.env` | ✅ |
| `FirstAgentTest.py` 全链路跑通 | ✅ |
| Python 核心语法（变量/控制流/函数/集合/异常） | ✅ |
| 装饰器（含三层嵌套、property、args/kwargs） | ✅ |
| 类型注解 + typing 模块 | ✅ |
| pydantic + f-string（`w2_01`/`w2_02`） | ✅ |
| async/await + dataclasses（`w2_03`） | ✅ 已验收 |
| with 上下文管理器 + pytest（`w2_04`，20 测试通过） | ✅ 已验收 |
| **高频核心语法**（推导式/生成器/魔术方法/lambda/Enum，`w2_05`） | ✅ 已验收 |
| **工程化补充**（pathlib/functools/解包，`w2_06`） | ✅ 已验收 |
| **现代语法**（walrus/match-case/`__slots__`/itertools，`w2_07`） | ✅ 已验收 |

> 🎉 **Python 语法阶段全部完成**（w1_01 → w2_07，共 12 个练习文件，全部运行验收通过）。下一步进 Ch1 理论。

---

## 🗓️ 4 周总览

| 周 | 主题 | 章节 | 核心产出 | 强度 |
|----|------|------|---------|------|
| **第 1 周** | 语法收尾 + 理论奠基 | Python 剩余 + Ch1-4 | 第一个自写 ReAct Agent | 🔴 密集 |
| **第 2 周** | 单体智能体构建 | Ch5-7 | 自建 Agent 框架 | 🔴🔴 核心 |
| **第 3 周** | 高级能力 + 训练 | Ch8-12 | MCP 服务 + 模型训练 | 🔴🔴🔴 最难 |
| **第 4 周** | 综合实战 + 毕业 | Ch13-16 | 全栈项目 + PR | 🟠 实战 |

---

# 📕 第 1 周：语法收尾 + 理论奠基（Day 1-7）

> 📖 **本周避坑**：[`PITFALLS-GUIDE.md` 第一篇（Python 语言层）+ 第二篇（工程化）+ 第三篇（Agent 核心误解）](./PITFALLS-GUIDE.md)

## 本周目标
- 完成 Python 语法补强（async/dataclass/pytest）
- 跑通 Ch1-3 理论，建立 LLM 心智模型
- **亲手写出第一个 ReAct Agent**（本周最大产出）

## Day 1（周一）— Python 语法收尾 A
**任务**：async/await 协程 + dataclasses
- [ ] 学 `async/await` 基础（`code/learn/` 待生成练习）
  - async def / await / asyncio.run() 三件套
  - 对比 Java CompletableFuture / Reactor
  - 理解 Ch7 异步工具、Ch11 分布式训练为何用 async
- [ ] 学 `dataclasses`（轻量数据类，类比 Java Record）
  - `@dataclass` 装饰器
  - 对比 pydantic BaseModel：何时用 dataclass、何时用 pydantic
- [ ] **练习文件**：`code/learn/w2_03_async_dataclass.py`（待生成）
- **验收**：能写出一个 async 函数并发调用 2 个 mock API

## Day 2（周二）— Python 语法收尾 B
**任务**：with 上下文管理器 + pytest
- [ ] 学 `with` 语句（资源管理，类比 Java try-with-resources）
  - `__enter__` / `__exit__` 协议
  - contextlib.contextmanager 装饰器写法
- [ ] 学 pytest 基础（Ch7 有完整 test_*.py）
  - `def test_xxx()` 命名约定
  - `assert` 断言
  - fixture（`@pytest.fixture`，类比 JUnit @BeforeEach）
  - 参数化测试 `@pytest.mark.parametrize`
- [ ] **练习文件**：`code/learn/w2_04_with_pytest.py`（待生成）
- **验收**：能看懂 Ch7 的 `test_simple_agent.py` 结构

## Day 3（周三）— Ch1 初识智能体
**任务**：建立 Agent 概念框架
- [ ] 读 `docs/chapter1/第一章 初识智能体.md`（663 行，约 1.5 小时）
- [ ] **重点理解**：
  - Agent 定义（感知-思考-行动循环）
  - PEAS 任务环境模型
  - Agent 分类（反射/目标/效用/学习型）
  - LLM Agent 架构（Brain + Perception + Action）
- [ ] **重读** `code/chapter1/FirstAgentTest.py`（已跑通）
  - 对照理论，理解 Thought-Action-Observation 循环
  - 用你的 Java 经验理解：Agent 主循环 = Web 服务的请求处理循环
- **验收**：能用大白话向同事讲清「什么是 AI Agent」

## Day 4（周四）— Ch2 智能体发展史
**任务**：建立历史脉络（快读，不深抠）
- [ ] 读 `docs/chapter2/第二章 智能体发展史.md`（568 行，约 1 小时）
- [ ] **重点理解**（只抓主线）：
  - 符号主义（专家系统/MYCIN）→ 连接主义（神经网络）→ RL（AlphaGo）→ LLM Agent
  -涌现能力、CoT 思维链
- [ ] 跑 `code/chapter2/ELIZA.py`（早期聊天机器人，体验规则匹配）
- [ ] **策略**：历史章节快读+笔记，不深抠代码
- **验收**：能画出 Agent 发展时间线（一页纸）

## Day 5-6（周五-周六）— Ch3 大语言模型基础 🔴 理论难点
**任务**：理解 LLM 工作原理（本周最重）
- [ ] 读 `docs/chapter3/第三章 大语言模型基础.md`（1020 行，约 3 小时）
- [ ] **5 个脚本逐个跑**（`code/chapter3/`）：
  - [ ] `Word_Embedding.py` → 词向量概念
  - [ ] `N_gram.py` → 统计语言模型
  - [ ] `BPE.py` → 分词（理解 tokenizer）
  - [ ] `Transformer.py` → 🔴 **全书理论最难点**（注意力机制）
  - [ ] `Qwen.py` → 本地跑 Qwen 小模型推理
- [ ] **额外补理论**（周六集中看 2-3 小时）：
  - 李宏毅 Transformer 教程视频（B 站搜「李宏毅 Transformer」）
  - 或 Jay Alammar 的图解 Transformer 博客
- [ ] **你的 GPU 优势**：本地跑 Qwen 0.5B 体验推理延迟
- **验收**：能解释「什么是注意力机制」「为什么 LLM 会幻觉」

## Day 7（周日）— Ch4 经典范式构建（上）🔴 本周核心产出
**任务**：手写第一个 Agent 范式（不依赖任何框架）
- [ ] 读 `docs/chapter4/第四章 智能体经典范式构建.md` 前 600 行
- [ ] **手写 ReAct 范式**（`code/chapter4/ReAct.py`）：
  - [ ] 先读懂 `llm_client.py`（OpenAI 兼容客户端封装）
  - [ ] 读懂 `tools.py`（工具定义模式）
  - [ ] 跑通 `ReAct.py`，观察 Reason + Act 循环
  - [ ] **改造练习**：给 ReAct 加一个你自己的工具（如调一个你熟悉的接口）
- [ ] **Java 迁移点**：ReAct 循环 = Web 服务的「请求路由→调下游→处理响应→再路由」
- **验收**：ReAct Agent 能完成多步推理任务（至少 2 次工具调用）

---

# 📗 第 2 周：单体智能体构建（Day 8-14）

> 📖 **本周避坑**：[`PITFALLS-GUIDE.md` 第四篇（LLM API 调用）+ 第五篇（Ch7 框架设计·Java 架构师专项）](./PITFALLS-GUIDE.md)

## 本周目标
- 体验低代码平台（1 天速通）
- 对比 4 大框架（理解轮子怎么造）
- **自建 Agent 框架 HelloAgents**（本周最大产出，全书工程核心）

## Day 8（周一）— Ch4 收尾 + Ch5 低代码（上）
**任务**：完成剩余 2 个范式 + 开始低代码
- [ ] Ch4 收尾：
  - [ ] `Plan_and_solve.py`（先规划后执行）
  - [ ] `Reflection.py`（自我反思）
- [ ] Ch5 开始：读 `docs/chapter5/第五章 基于低代码平台的智能体搭建.md` 前 400 行
- **验收**：3 个范式都能跑通，理解差异

## Day 9（周二）— Ch5 低代码平台 🟢 你的舒适区
**任务**：4 平台各做 1 案例（你的 Web 经验让你秒懂）
- [ ] 读 Ch5 剩余部分（1271 行，选重点）
- [ ] **4 平台实战**（每个约 30 分钟）：
  - [ ] **Coze**：导入 `code/chapter5/HelloAgent_cozeCase.zip`，建「每日 AI 简报」
  - [ ] **Dify**：导入 `HelloAgent_difyCase.yml`，参考 `Extra-Chapter/Extra03` 保姆教程
  - [ ] **FastGPT**：导入 `HelloAgent_fastgptCase.json`，建智能投资顾问（RAG）
  - [ ] **n8n**：按 `Additional-Chapter/N8N_INSTALL_GUIDE.md` 用 Docker 装，建邮件助手
- [ ] **策略**：用你的 Web 服务理解看透这些平台的本质（可视化 API 编排）
- **验收**：至少 2 个平台能跑通完整案例

## Day 10（周三）— Ch6 框架实践（上）
**任务**：对比主流框架（理解轮子）
- [ ] 读 `docs/chapter6/第六章 框架开发实践.md` 前 700 行
- [ ] **AutoGen**（`code/chapter6/AutoGenDemo/`）：软件开发团队多角色
  - [ ] `pip install autogen-agentchat autogen-ext[openai]`
  - [ ] 跑通多 Agent 对话
- [ ] **AgentScope**（`code/chapter6/AgentScopeDemo/`）：狼人杀游戏
  - [ ] `pip install agentscope`
  - [ ] 体验多 Agent 投票/辩论
- **验收**：2 个框架跑通，理解多 Agent 协作模式

## Day 11（周四）— Ch6 框架实践（下）
**任务**：完成 CAMEL + LangGraph
- [ ] **CAMEL**（`code/chapter6/CAMEL/`）：AI 科普电子书
  - [ ] `pip install camel-ai`
  - [ ] 体验角色扮演式协作
- [ ] **LangGraph**（`code/chapter6/Langgraph/`）🔴 重点（对你理解 Ch7 框架架构最有帮助）
  - [ ] `pip install langgraph langchain-openai`
  - [ ] 跑通状态图（planner→executor 节点 + 条件边）
  - [ ] 理解 StateGraph 思想（类比 Java 的工作流引擎）
- **验收**：LangGraph 状态图能跑通，理解「节点+边」的设计

## Day 12-13（周五-周六）— Ch7 自建 Agent 框架 🔴🔴 全书工程核心
**任务**：从零造一个叫 HelloAgents 的框架（你的 Java 架构经验全面发力）
- [ ] 读 `docs/chapter7/第七章 构建你的Agent框架.md`（2200 行，分 2 天）
- [ ] **装框架**：`pip install hello-agents`
- [ ] **代码逐步吃透**（`code/chapter7/`，12 个 py 文件）：
  - [ ] Day 12：`my_llm.py`（多 provider LLM 抽象）→ `my_simple_agent.py`（SimpleAgent）
    - 重点：抽象基类设计（Message/Config/Agent ABC，类比 Java interface）
    - 重点：多 provider 自动检测（OpenAI/Ollama/vLLM）
  - [ ] Day 13：`my_react_agent.py`（ReActAgent）→ 工具系统（`my_calculator_tool.py`、`my_advanced_search.py`）
    - 重点：工具注册机制（你学过的装饰器！`@register_tool`）
    - 重点：Function Call Agent（OpenAI 原生函数调用）
    - 重点：异步工具执行
- [ ] **跑通测试**：`pytest code/chapter7/test_*.py -v`（6 个测试文件）
- **验收**：能用自建框架跑一个多工具 Agent，并写一个新工具注册进去

## Day 14（周日）— Ch7 扩展 + 缓冲日
**任务**：消化 Ch7 + 给自己留缓冲
- [ ] 给框架扩展一个新 Agent 类型（如 SimpleAgent 的变体）
- [ ] 写一个新工具并用 `@register_tool` 注册
- [ ] 整理本周笔记
- [ ] 如果前面有落后，今天补上
- **验收**：能不看书复述 HelloAgents 框架的抽象层次

---

# 📘 第 3 周：高级能力 + 训练（Day 15-21）

> 📖 **本周避坑**：[`PITFALLS-GUIDE.md` 第六篇（向量/RAG·SQL 迁移）+ 第七篇（模型训练·认知颠覆）+ 第八篇（异步 async）](./PITFALLS-GUIDE.md)

## 本周目标
- 掌握记忆与 RAG 全流程
- 理解上下文工程
- **建一个 MCP 服务器**（你的 Web 主场）
- **本地 GPU 跑通模型训练**（全书最难，周末集中攻克）

## Day 15（周一）— Ch8 记忆与检索（上）🔴
**任务**：记忆系统 + 向量数据库
- [ ] 读 `docs/chapter8/第八章 记忆与检索.md` 前 1000 行
- [ ] **启动 Docker Desktop**，准备数据库
- [ ] **Docker 起 Qdrant**（向量库）：
  ```bash
  docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
  ```
- [ ] 跑 `code/chapter8/` 脚本 1-5：
  - [ ] `01_MemoryTool_Basic_Operations.py`（记忆 CRUD）
  - [ ] `02`-`05`：记忆类型（工作/情景/语义/感知）
- [ ] **你的 SQL 经验**：向量检索 = `ORDER BY cosine_similarity DESC LIMIT k`，类比 KNN
- **验收**：Qdrant 能存取向量

## Day 16（周二）— Ch8 记忆与检索（下）🔴 RAG 流程
**任务**：RAG 全流程
- [ ] 读 Ch8 剩余部分
- [ ] **Neo4j 图数据库**（用 Aura 免费云版，或 Docker）
- [ ] 跑 `code/chapter8/` 脚本 6-11：
  - [ ] `06`-`08`：RAG 摄入（MarkItDown）→ 分块 → 向量化（embeddings）
  - [ ] `09`-`10`：检索 + 高级检索策略
  - [ ] `11_Q&A_Assistant.py`：完整 RAG 问答助手
- [ ] **产出**：用自己的文档（如你的笔记）做一次 RAG 问答
- **验收**：RAG 助手能基于你的文档回答问题

## Day 17（周三）— Ch9 上下文工程
**任务**：长程任务的上下文管理
- [ ] 读 `docs/chapter9/第九章 上下文工程.md`（2819 行，选重点约 1500 行）
- [ ] **代码**（`code/chapter9/`）：
  - [ ] `ContextBuilder`（GSSC 流水线）
  - [ ] `NoteTool`（结构化笔记存文件系统）
  - [ ] `TerminalTool`（沙箱 shell，命令白名单 + 超时限制）
- [ ] 跑通「代码库维护助手」三天工作流模拟
- [ ] **基于 Ch7 框架扩展**，所以确保 Ch7 学扎实
- **验收**：能解释「上下文工程和 RAG 的区别」

## Day 18（周四）— Ch10 通信协议（MCP）🔴🔴 你的主场
**任务**：MCP 协议 + 建自己的 MCP 服务器
- [ ] 读 `docs/chapter10/第十章 智能体通信协议.md` 前 1200 行
- [ ] **MCP（Model Context Protocol）**——行业新标准：
  - [ ] 用 MCP 客户端调社区服务器（GitHub MCP、天气 MCP）
  - [ ] 理解 5 种传输：memory/stdio/HTTP/SSE/StreamableHTTP
  - [ ] **你的优势**：MCP 服务端 = HTTP/RPC 服务，用你 7 年 Web 经验对照秒懂
- [ ] 跑 `code/chapter10/` 脚本 1-10（MCP 部分）
- **验收**：能用 MCP 客户端调通一个社区服务器

## Day 19（周五）— Ch10 通信协议（A2A/ANP）+ 建 MCP 服务器
**任务**：完成协议 + 动手建服务
- [ ] 读 Ch10 剩余（A2A + ANP）
- [ ] **A2A**（Agent-to-Agent）：Agent 作为服务暴露、多 Agent 协作
  - **类比微服务**：每个 Agent = 一个微服务，A2A = 服务间调用
- [ ] **ANP**（Agent Network Protocol）：服务发现、负载均衡
  - **类比 Eureka/Nacos** 注册中心
- [ ] **动手建 MCP 服务器**（`code/chapter10/my_mcp_server.py` + `weather-mcp-server/`）：
  - [ ] 跑通天气 MCP 服务器
  - [ ] 用 Docker 化部署（含 Dockerfile）
  - [ ] 可选：上传 Smithery
- **验收**：你建的 MCP 服务器能被 Agent 调用

## Day 20-21（周六-周日）— Ch11 Agentic-RL 🔴🔴🔴 全书最硬核
**任务**：本地 GPU 跑通 SFT → GRPO 训练（全书唯一可能让你想放弃的章节）
- [ ] **Day 20 上午：补 DL 基础**（2-3 小时视频）
  - 3Blue1Brown 神经网络系列（理解反向传播）
  - 李宏毅 RL 课程 2-3 集（理解 PPO→GRPO）
- [ ] 读 `docs/chapter11/第十一章 Agentic-RL.md`（2687 行，分 2 天）
- [ ] **Day 20 下午-21：实战训练**（`code/chapter11/`，9 个脚本）：
  - [ ] `00_quick_test.py`：环境验证
  - [ ] `01`-`03`：SFT 监督微调（LoRA，r=8/alpha=16）
    - 数据集 `gsm8k`，基座 `Qwen/Qwen3-0.6B`
    - **你的 GPU（RTX 4060 8GB）能跑 0.6B 模型**
  - [ ] `04`-`06`：GRPO 强化学习（KL=0.1）
  - [ ] `07`：超参搜索（Optuna）
  - [ ] `08_distributed_training.py`：分布式（DeepSpeed，理解原理即可）
- [ ] **监控**：TensorBoard 看训练曲线
- [ ] **部署**：LoRA 合并 + 8-bit 量化 + FastAPI 服务化
- [ ] **心态**：允许慢，允许调参失败，理解流程 > 刷指标
- **验收**：GPU 上完整跑通一次 SFT 训练，能看到 loss 下降

---

# 📙 第 4 周：综合实战 + 毕业（Day 22-28）

> 📖 **本周避坑**：[`PITFALLS-GUIDE.md` 第九篇（前端 Vue·后端的恐惧）+ 第十篇（Agent 调试心法）](./PITFALLS-GUIDE.md)

## 本周目标
- 跑通评估系统（Ch12）
- 完成 2 个全栈项目（Ch13/14）
- 体验 Ch15 游戏 Agent
- **提交毕业设计 PR**（最终产出）

## Day 22（周一）— Ch12 性能评估
**任务**：评估 Agent 质量
- [ ] 读 `docs/chapter12/第十二章 智能体性能评估.md`（2743 行，选重点）
- [ ] **三大 benchmark**：
  - [ ] **BFCL**（函数调用能力）：跑 `bfcl-eval`，测你 Ch4-7 写的 Agent
  - [ ] **GAIA**（真实任务）：下载 HuggingFace 数据集
  - [ ] **LLM-as-Judge / Win-Rate**：数据质量评估
- [ ] 跑 `code/chapter12/` 脚本 1-5
- **验收**：能用评估系统测一个 Agent 的函数调用准确率

## Day 23-24（周二-周三）— Ch13 智能旅行助手 🔴 全栈项目 1
**任务**：MCP + 多 Agent + Vue 全栈（你的 Web 经验全面复用）
- [ ] 读 `docs/chapter13/第十三章 智能旅行助手.md`（1581 行）
- [ ] **申请 API Key**：
  - 高德地图 `AMAP_API_KEY`：https://lbs.amap.com
  - Unsplash `UNSPLASH_ACCESS_KEY`：https://unsplash.com/developers
- [ ] **后端**（`code/chapter13/helloagents-trip-planner/backend/`，亲手做）：
  - [ ] Pydantic 数据建模（你已掌握！）
  - [ ] 多 Agent 协作（角色设计 + 查询构建）
  - [ ] MCP 工具集成（高德，1 个 MCPTool → 16 个工具）
  - [ ] FastAPI 后端（你熟悉 Spring Boot 的话，FastAPI 路由/依赖注入/异步很好懂）
- [ ] **前端**（`frontend/`，亲手做）：Vue3 + TS + Vite + Ant Design Vue
  - [ ] `cd frontend && npm install`
  - [ ] 表单设计 + 结果展示 + 行程编辑 + PDF 导出
- **验收**：完整跑起来，输入目的地→多 Agent→生成带图行程→导出 PDF

## Day 25（周四）— Ch14 深度研究 Agent 🔴 全栈项目 2
**任务**：TODO 驱动的三阶段研究 Agent
- [ ] 读 `docs/chapter14/第十四章 自动化深度研究智能体.md`（2152 行）
- [ ] **用 uv 包管理器**（你已装 0.6.16）
- [ ] **后端**（`backend/`）：
  - [ ] 自定义 `ToolAwareSimpleAgent`
  - [ ] `SearchTool` / `NoteTool` / `ToolRegistry`
  - [ ] 服务层：任务规划 + 总结 + 报告生成 + 限流搜索
- [ ] **前端**（亲手做）：全屏 modal + 实时进度 + 结果可视化
- **验收**：给一个研究课题，自动搜索→笔记→生成报告

## Day 26（周五）— Ch15 赛博小镇 🟡（前端降级）
**任务**：Agent + 游戏（最复杂，但前端仅读代码）
- [ ] 读 `docs/chapter15/第十五章 构建赛博小镇.md`（1899 行）
- [ ] **后端**（`backend/`，亲手做）：
  - [ ] NPC Agent（基于 HelloAgents SimpleAgent）
  - [ ] SQLite 记忆系统集成
  - [ ] 批量对话生成（轻负载混合模式）
  - [ ] **好感度系统**（等级分类 + 计算逻辑 + 对话影响）
  - [ ] FastAPI + CORS + 状态管理
- [ ] **前端**（Godot + GDScript，**仅读代码理解架构**）：
  - [ ] 装 Godot 4.5，打开 `helloagents-ai-town/project.godot` 跑起来体验
  - [ ] 读 `api_client.gd`（理解后端 API 调用）
  - [ ] 不强求自己写 GDScript
- **验收**：后端亲手完成测试，前端跑通体验

## Day 27-28（周六-周日）— Ch16 毕业设计 🔴 收官
**任务**：独立设计并开源一个多 Agent 应用
- [ ] 读 `docs/chapter16/第十六章 毕业设计.md` + `code/chapter16/共创路径.md`
- [ ] **选题**（结合你的 Java Web 背景）：
  - 智能代码审查助手 / SRE 运维 Agent / 企业知识库 RAG 问答
- [ ] **流程**：
  - [ ] fork 仓库
  - [ ] 搭项目结构（`Co-creation-projects/你的用户名-项目名/`）
  - [ ] 写 README + requirements.txt
  - [ ] Jupyter Notebook 开发
  - [ ] 测试
  - [ ] 提 PR
- [ ] 参考 `Co-creation-projects/` 35 个学长作品
- **验收**：提交一个可运行的 PR

---

# 📋 每日时间分配建议（886 制）

## 工作日（周一至周五，约 1.5-2 小时）
```
20:30-21:00  读理论文档 (30 min)
21:00-22:00  跑代码/改代码 (60 min)  ← 核心时间
22:00-22:30  记笔记/整理 (30 min, 可选)
```

## 周末（周六-周日，每天约 5-6 小时）
```
09:00-12:00  深度实战 (3h)  ← 跑大项目/训练/全栈
14:00-17:00  深度实战 (3h)  ← 写代码/调 bug
晚上          整理笔记, 轻松复习
```

---

# 🎯 优先级矩阵（时间不够时砍什么）

## 🔴 必须深度掌握（不能跳）
| 内容 | 理由 |
|------|------|
| Ch4 ReAct 手写 | 所有 Agent 的基础范式 |
| Ch7 自建框架 | 全书工程核心，后续章节都基于它 |
| Ch10 MCP | 行业新标准，你的 Web 主场 |
| Ch11 SFT 训练 | 全书最值钱技能，AI 转型核心 |
| Ch13 全栈项目 | 综合实战，作品集 |

## 🟡 需要理解原理（代码跑通即可）
| 内容 | 策略 |
|------|------|
| Ch3 Transformer | 跑通代码 + 看视频，不纠结数学推导 |
| Ch6 四框架 | 跑通 + 理解差异，不必精通每个 |
| Ch12 评估 | 跑通 BFCL，GAIA 了解即可 |
| Ch14 深度研究 | 后端做，前端可简化 |

## 🟢 快速浏览（1 天内过完）
| 内容 | 策略 |
|------|------|
| Ch1-2 理论 | 快读+笔记 |
| Ch5 低代码 | 2 个平台跑通即可 |
| Ch15 Godot | 只读代码，不强求开发 |
| Extra 系列 | 选读 01/09/10，其余跳过 |

---

# ⚠️ 风险预警 + 应对

| 风险 | 概率 | 应对 |
|------|------|------|
| **Ch11 训练跑不通** | 高 | 先跑通最小 SFT（0.6B 模型），GRPO 可只理解原理；允许用现成 checkpoint |
| **Ch13/14 前端卡住** | 中 | 前端只做最小可用版本（表单+展示），不做 PDF 导出等高级功能 |
| **886 加班断更** | 中 | 用 Day 7/14/21/28 的缓冲日补；理论章可压缩到音频通勤听 |
| **某章深度不够** | 低 | 优先级矩阵保底：先保证 🔴 章节，🟢 章节可只读不练 |
| **4 周太紧** | 高 | 允许延长到 5 周；或在第 4 周末只完成 Ch13 + Ch16，Ch14/15 降级为阅读 |

---

# 📦 环境增量准备清单（按周）

## 第 1 周
- [ ] 无新增（环境已就绪）

## 第 2 周
- [ ] `pip install hello-agents`（Ch7 框架）
- [ ] `pip install autogen-agentchat agentscope camel-ai`（Ch6，按需装）
- [ ] 启动 Docker Desktop（Ch5 n8n）

## 第 3 周
- [ ] Docker 起 Qdrant + Neo4j（Ch8）
- [ ] `pip install fastmcp`（Ch10，已装）
- [ ] `pip install trl peft accelerate deepspeed optuna`（Ch11 训练）
- [ ] 注册 HuggingFace，设 `HF_TOKEN`（国内用 `hf-mirror.com`，已配）
- [ ] 可选：注册 W&B 监控训练

## 第 4 周
- [ ] 申请高德 API Key + Unsplash Key（Ch13）
- [ ] 装 Godot 4.5（Ch15 体验，可选）
- [ ] `pip install "hello-agents[protocols]>=0.2.4,<=0.2.9"`（Ch13/15 版本要求）

---

# ✅ 每周验收标准

## 第 1 周末
- [ ] Python async/dataclass/pytest 能写能用
- [ ] Ch1-3 理论能讲清核心概念
- [ ] **第一个 ReAct Agent 跑通**

## 第 2 周末
- [ ] 2 个低代码平台跑通
- [ ] LangGraph 状态图跑通
- [ ] **自建 HelloAgents 框架能跑多工具 Agent**

## 第 3 周末
- [ ] RAG 问答助手跑通
- [ ] **自建 MCP 服务器部署成功**
- [ ] **GPU 跑通一次 SFT 训练**

## 第 4 周末
- [ ] Ch13 旅行助手全栈跑通
- [ ] **毕业设计 PR 提交**
- [ ] 能独立设计一个多 Agent 应用

---

# 📌 立即行动

**今天（Day 1）就开始**：
1. 完成剩余的 pydantic 深度练习（`w2_02_pydantic_deep.py`）
2. 做 async/dataclass 练习（我会生成 `w2_03`）
3. 周三前进入 Ch1 理论

**记住**：这份计划很激进，**允许调整**。如果某周没完成，优先保证 🔴 章节。Ch11 训练和 Ch7 框架是两个绝对不能跳的核心。
