# Hello-Agents 学习计划（v2 — 环境实测后调整版）

> 为你定制：Java Web 服务开发（886），目标「全面系统掌握」
> 周期：**约 29 周 / 7 个月**（12-15 小时/周）
> 硬件：RTX 4060 8GB（Ch11 本地实战）｜前端：Vue 亲手做，Godot 仅读代码
> 主环境：conda `hello-agents`（Python 3.10）

---

## v2 相比 v1 的调整说明

| 调整项 | v1（预估） | v2（实测后） | 原因 |
|--------|-----------|-------------|------|
| 环境搭建 | W3 整周 | 压缩到 W1 半天 | 实测环境已远超需求（GPU+CUDA+全套AI包+uv） |
| Python 地基 | W1-W3（3周） | W1-W2（2周） | 环境省掉，只补语法（装饰器/类型注解/async/pydantic） |
| Ch11 训练 | 2 周 | **3 周** | 省下的 1 周加到全书最难章 |
| 总周期 | 30 周 | **29 周** | - |

---

## 🗓️ 阶段总览（29 周）

| 阶段 | 周数 | 内容 | 强度 |
|------|------|------|------|
| **第 0 阶段：Python 语法补强** | W1-W2 | 装环境+补语法 | 🔴 |
| **第 1 阶段：理论与基础** | W3-W6 | Ch1-3 | 🟡 |
| **第 2 阶段：单体智能体** | W7-W13 | Ch4-7 | 🔴 核心 |
| **第 3 阶段：高级能力** | W14-W20 | Ch8-12 | 🔴 最难 |
| **第 4 阶段：综合实战** | W21-W26 | Ch13-15 | 🟠 |
| **第 5 阶段：毕业与拓展** | W27-W29 | Ch16 + Extra | 🟢 |

---

## 第 0 阶段：Python 语法补强（W1-W2）🔴

> 环境已就绪，重点补「写 Agent 代码的刚需语法」，用 Java 经验做迁移。

### W1：环境激活 + 语法核心
- [ ] **Day1 半天**：新建 `hello-agents` conda 环境（见 `ENV-REPORT.md` 第三节命令），配 AIHubmix/Tavily API Key，跑通 `code/chapter1/FirstAgentTest.py`
- [ ] **Day1-2**：Python 核心语法（变量/控制流/函数/集合/异常）——对照 Java
- [ ] **Day3-5**：**装饰器**（`@staticmethod`/`@property`/自定义）+ **类型注解**（`Optional`/`List[Dict]`/`Callable`）——Ch7 框架核心
- [ ] **周末**：逐行读懂 `FirstAgentTest.py`，写一个调 wttr.in 的天气脚本

### W2：进阶特性（Agent 开发密集用到的）
- [ ] **f-string 与 prompt 拼接**（Agent 的 System Prompt 核心技能）
- [ ] **`pydantic` 数据建模**（Ch7/13 核心，类比 Java POJO + Lombok）
- [ ] **`async/await` 协程**（Ch7 异步工具、Ch11 分布式训练）
- [ ] **`dataclasses` + `with` 上下文管理器**
- [ ] **pytest 基础**（Ch7 有 `test_*.py`）
- [ ] **产出**：用 pydantic 写「用户订单」模型 + 一个 async 函数 + pytest 测试

---

## 第 1 阶段：理论与基础（W3-W6）🟡

### W3：Ch1 初识智能体
- [ ] 读 `docs/chapter1/第一章 初识智能体.md`
- [ ] 重点：Agent 定义、感知-思考-行动循环、PEAS、Agent 分类
- [ ] 深读 `FirstAgentTest.py`（Thought-Action-Observation 文本解析）
- [ ] 你的优势点：工具调用 = Web 服务的 API 调度

### W4：Ch2 智能体发展史
- [ ] 读 `docs/chapter2/第二章 智能体发展史.md`
- [ ] 跑 `code/chapter2/ELIZA.py`
- [ ] 1 周读完+笔记即可

### W5-W6：Ch3 大语言模型基础 🟠 补 ML 理论
- [ ] 读 `docs/chapter3/第三章 大语言模型基础.md`
- [ ] 5 个脚本逐个吃透：`Word_Embedding.py` → `N_gram.py` → `BPE.py` → `Transformer.py`（🔴 全书理论最难点）→ `Qwen.py`
- [ ] **额外补**：2-3 个晚上看「Attention is All You Need」图解 / 李宏毅 Transformer 视频
- [ ] 本地 GPU 跑 Qwen 0.5B 体验推理

---

## 第 2 阶段：单体智能体（W7-W13）🔴 核心阶段

### W7-W8：Ch4 经典范式构建 🔴
- [ ] 读 `docs/chapter4/第四章 智能体经典范式构建.md`
- [ ] 手写三大范式：`ReAct.py`（W7上）→ `Plan_and_solve.py`（W7下）→ `Reflection.py`（W8）
- [ ] 吃透 `llm_client.py` + `tools.py` + prompt 模板
- [ ] **产出**：给 ReAct 加一个自定义工具（调你熟悉的 Java 接口）

### W9：Ch5 低代码平台 🟢 你的舒适区
- [ ] 读 `docs/chapter5/第五章 基于低代码平台的智能体搭建.md`
- [ ] 启动 Docker Desktop，按 `Additional-Chapter/N8N_INSTALL_GUIDE.md` 装 n8n
- [ ] 4 平台各 1 案例：Coze / Dify（参考 Extra03）/ FastGPT / n8n
- [ ] Web 背景让你能秒懂这些平台本质（可视化编排）

### W10-W11：Ch6 框架开发实践 🟡
- [ ] 读 `docs/chapter6/第六章 框架开发实践.md`
- [ ] 4 框架对比：AutoGen（W10上）→ AgentScope（W10下）→ CAMEL（W11上）→ LangGraph（W11下）
- [ ] 按需装 `autogen` / `agentscope` / `camel-ai`
- [ ] 目标：跑通+理解差异，为 Ch7 造框架铺垫

### W12-W13：Ch7 构建你的 Agent 框架 🔴🔴 全书工程核心
> 你 7 年 Web 架构经验在这里是巨大优势。

- [ ] 读 `docs/chapter7/第七章 构建你的Agent框架.md`
- [ ] `pip install hello-agents`（或参考自建版代码 `code/chapter7/`）
- [ ] 吃透：`my_llm.py`（多 provider 抽象）→ `my_simple_agent.py` → `my_react_agent.py` → 工具系统
- [ ] 重点：抽象基类（Message/Config/Agent ABC，类比 Java interface）、工具注册机制、Function Call Agent、异步工具链
- [ ] 跑通所有 `test_*.py`
- [ ] **产出**：扩展一个新 Agent 类型 + 新工具 + pytest 验证

---

## 第 3 阶段：高级能力（W14-W20）🔴 全书最难

### W14-W15：Ch8 记忆与检索 🔴
- [ ] 读 `docs/chapter8/第八章 记忆与检索.md`
- [ ] Docker 启动 Qdrant（向量库）+ Neo4j（图库，可用 Aura 云端）
- [ ] 11 个脚本逐个跑（`01_*.py` → `11_*.py`）：摄入→分块→向量化→存储→检索
- [ ] 你的 SQL 优势点：向量库/图库类比关系型 DB
- [ ] **产出**：用自己的文档跑 `11_Q&A_Assistant.py` RAG 问答

### W16：Ch9 上下文工程 🟡
- [ ] 读 `docs/chapter9/第九章 上下文工程.md`
- [ ] `ContextBuilder`（GSSC 流水线）+ `NoteTool` + `TerminalTool`（沙箱）
- [ ] 基于 Ch7 框架扩展
- [ ] **产出**：跑通「代码库维护助手」三天工作流

### W17-W18：Ch10 通信协议 🟢 你的绝对主场 🔴🔴
> MCP/A2A/ANP = Agent 如何像 Web 服务一样提供/消费 API。为你量身定做。

- [ ] 读 `docs/chapter10/第十章 智能体通信协议.md`
- [ ] **MCP**（最重要，行业新标准）：客户端调社区服务器 → 理解 5 种传输（memory/stdio/HTTP/SSE/StreamableHTTP）→ **建自己的 MCP 服务器**（`my_mcp_server.py` + `weather-mcp-server/`，Docker 化上 Smithery）
- [ ] **A2A**：Agent 作为服务、多 Agent 协作/谈判、客服路由
- [ ] **ANP**：服务发现、能力匹配、负载均衡（类比微服务注册中心）
- [ ] **产出**：建一个 MCP 服务器（包装你熟悉的 Java API），Docker 部署

### W19-W21：Ch11 Agentic-RL 🔴🔴🔴 全书最硬核（已扩到 3 周）
> 你有 GPU，按完整实战学。先补 DL 基础。

- [ ] **W19（预备）**：补 DL 最小必要知识——反向传播、梯度下降、PyTorch 基础、LoRA、PPO→GRPO（3B1B 神经网络系列 + 李宏毅 RL 课 2-3 集）
- [ ] 读 `docs/chapter11/第十一章 Agentic-RL.md`
- [ ] 9 个脚本（`00_quick_test.py` → `08_distributed_training.py`）：
  - SFT 监督微调 + LoRA（r=8/alpha=16）
  - GRPO（KL=0.1，4 generations）
  - 数据集 `gsm8k`，基座 `Qwen/Qwen3-0.6B`（你的 GPU 能跑）
  - 分布式：DeepSpeed ZeRO-2/3、DDP（`accelerate_configs/`）
  - 超参搜索：网格 + Optuna
  - 部署：LoRA 合并、8-bit 量化、FastAPI 服务化
- [ ] TensorBoard + 可选 W&B 监控
- [ ] **产出**：本地 GPU 完整跑通 SFT→GRPO 训练 Qwen 小模型 + 部署 API
- [ ] **心态**：允许慢，允许失败，理解流程 > 刷指标

### W20（与 Ch11 交错后半周）：Ch12 性能评估 🟡
- [ ] 读 `docs/chapter12/第十二章 智能体性能评估.md`
- [ ] BFCL（函数调用）+ GAIA（真实任务）+ LLM-as-Judge/Win-Rate
- [ ] **产出**：用 HelloAgents 评估系统测你 Ch4-7 的 Agent 准确率

---

## 第 4 阶段：综合实战（W21-W26）🟠

### W21-W22：Ch13 智能旅行助手 🔴
- [ ] 读 `docs/chapter13/第十三章 智能旅行助手.md`
- [ ] 申请：高德 `AMAP_API_KEY`、Unsplash `UNSPLASH_ACCESS_KEY`
- [ ] 后端（亲手做）：Pydantic 建模、多 Agent 协作、MCP（高德，1→16 工具）、FastAPI
- [ ] 前端（亲手做）：Vue3+TS+Vite+Ant Design Vue+高德地图+PDF 导出
- [ ] **产出**：输入目的地→多 Agent 协作→带图行程→导出 PDF

### W23-W24：Ch14 深度研究 Agent 🔴
- [ ] 读 `docs/chapter14/第十四章 自动化深度研究智能体.md`
- [ ] 用 `uv` 包管理（你已装 0.6.16）
- [ ] 后端：`ToolAwareSimpleAgent`、`ToolRegistry`、服务层（规划/总结/报告/限流搜索）
- [ ] 多 LLM 支持：OpenAI/DeepSeek/Qwen/本地 Ollama（可选装）
- [ ] 前端（亲手做）：全屏 modal + 实时进度 + 结果可视化
- [ ] **产出**：给研究课题，自动搜索→笔记→报告

### W25-W26：Ch15 赛博小镇 🟡（前端降级）
- [ ] 读 `docs/chapter15/第十五章 构建赛博小镇.md`
- [ ] 后端（亲手做）：NPC Agent、SQLite 记忆、批量对话、**好感度系统**、FastAPI+CORS
- [ ] 前端（仅读代码）：Godot 4.5 打开 `project.godot` 体验，看 `api_client.gd`/`main.gd` 理解交互，不强求写 GDScript
- [ ] **产出**：后端亲手完成测试，前端跑通体验

---

## 第 5 阶段：毕业与拓展（W27-W29）🟢

### W27：Ch16 毕业设计 🔴 收官
- [ ] 读 `docs/chapter16/第十六章 毕业设计.md` + `code/chapter16/共创路径.md`
- [ ] 选题 → fork → 搭项目结构（`Co-creation-projects/用户名-项目名/`）→ README+requirements → Jupyter 开发 → 测试 → 提 PR
- [ ] 参考 35 个学长作品找灵感
- [ ] **选题建议**（结合 Java Web 背景）：智能代码审查 / SRE 运维 Agent / 企业知识库 RAG
- [ ] **产出**：提交 PR

### W28-W29：Extra 精选 + 查漏补缺 🟢
- [ ] **必读**：Extra01 面试题+答案（求职必备）/ Extra02 上下文工程补充 / Extra09 开发踩坑 / Extra10 Agent 自进化（串联复习全书）
- [ ] **选读**：Extra05 Skills vs MCP / Extra06 GUI Agent / Extra11 Web Agent / Extra12 旅行助手后训练

---

## ✅ 每章验收标准

- **理论章**（Ch1,2,3,5 部分）：能用大白话讲清核心概念 + 结构化笔记
- **代码章**：配套代码亲手跑通 + 至少改写一处 + 能解释关键行
- **框架章**（Ch7）：能不看书复述框架抽象层次
- **训练章**（Ch11）：本地 GPU 完整跑通 SFT→GRPO
- **项目章**（Ch13,14）：前后端跑起来 + 演示核心功能
- **毕业章**（Ch16）：提交 PR 到 `Co-creation-projects/`

---

## ⚠️ 关键风险与应对

| 风险 | 应对 |
|------|------|
| Python 语法不熟（最大风险） | W1-W2 装饰器/类型注解/async/pydantic 必须过关；后续遇到不懂语法随时回查 |
| Ch3 Transformer + Ch11 RL 理论门槛 | 允许「先跑通代码理解输入输出，再补理论」；别被数学推导卡住 |
| Ch11 训练耗时长/调参难 | 用 0.6B 模型；接受首次跑不出好效果；理解流程 > 刷指标 |
| 886 疲惫断更 | 工作日只读理论+少量代码，重代码集中周末；每 4 周设「机动周」补欠账 |
| 多 conda 环境混乱 | 统一用 `hello-agents` 环境，base 勿用于训练 |

---

## 📌 立即行动（今天就做）

> ✅ **磁盘策略已就绪**：所有大数据（模型/数据集/缓存）已重定向到 G 盘，conda 环境建在 D 盘，C 盘不再承受写入。详见 `ENV-REPORT.md` 的「磁盘空间与缓存策略」。

1. **创建主环境**（新开一个 Anaconda Prompt 或 PowerShell 窗口执行，确保读到最新环境变量）：
   ```bash
   conda create -n hello-agents python=3.10 -y
   conda activate hello-agents
   pip install openai requests python-dotenv tavily-python jupyter pytest
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
   python -c "import torch; print(torch.cuda.is_available())"  # 应为 True
   python -c "import os; print(os.environ.get('HF_HOME'))"     # 应为 G:\ProgramData\...
   ```

2. **注册 API Key**（按 `Extra-Chapter/Extra07-环境配置.md`）：
   - AIHubmix：https://aihubmix.com （免费 GLM，推荐）
   - Tavily：https://tavily.com （免费搜索）

3. **跑通验证**：用新环境跑 `code/chapter1/FirstAgentTest.py`，看到 Agent 正常推理即环境就绪。

4. **开始 W1 Python 语法补强**（装饰器 + 类型注解 + pydantic + async）。
