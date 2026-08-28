# 本地环境体检报告

> 生成日期：2026-07-12
> 用途：Hello-Agents 项目学习前的环境确认。结论：**环境远超项目需求，可直接开始学习**。

---

## 一、总览（绿灯项 ✅）

### Python 运行环境
| 项 | 现状 | 项目需求 | 状态 |
|---|---|---|---|
| Python 版本 | 3.12.13 (base) / 3.10.20 (py310) / 3.13.13 (tradingagents) | 3.10+ | ✅ 超额 |
| pip | 26.0.1 | - | ✅ |
| uv | 0.6.16 | Ch14 用 | ✅ 已装 |
| conda | Anaconda3 | 可选 | ✅ |
| pip 镜像 | 阿里云源（全局已配） | 国内加速 | ✅ |

### GPU / CUDA（Ch11 训练关键）
| 项 | 现状 | 状态 |
|---|---|---|
| GPU | NVIDIA RTX 4060 Laptop 8GB | ✅ 达标 |
| 驱动 | 596.49 (CUDA 13.2) | ✅ 最新 |
| CUDA Toolkit | nvcc 12.9 | ✅ |
| PyTorch (py310 环境) | **2.8.0+cu128，CUDA 可用** ✅ | ✅ 完美 |
| PyTorch (base 环境) | 2.9.1+cpu（无 CUDA） | ⚠️ 训练勿用 base |

### AI/ML 核心包（base 环境已预装）
- openai 2.24.0, langchain 1.2.10, langgraph 1.0.10
- fastapi 0.134, uvicorn 0.40, pydantic 2.12
- transformers 4.53, accelerate 1.13, peft 0.19
- sentence-transformers 5.5.1, huggingface_hub 0.36.2
- **fastmcp 3.4.2**（Ch10 MCP 核心）
- jupyter/jupyterlab, pytest, ruff, mypy, streamlit, loguru, httpx
- numpy 2.2.6, pandas 2.3.3, scikit-learn 1.8.0, matplotlib 3.10.8
- py310 环境额外有：tavily-python 0.5.3, torch+cu128

### 开发工具链
- **IDE**：VS Code + PyCharm + WebStorm + IntelliJ IDEA ×2 + HBuilderX
- Git 2.53（已配本项目 origin）
- Node.js v24.15.0 + npm 11.12（Ch13/14 前端就绪）
- Docker 29.3.1（已装，但守护进程需手动启动）
- Apifox（API 调试）、Cherry Studio（模型测试）
- 磁盘：详见下方「磁盘空间与缓存策略」

### 磁盘空间与缓存策略（已配置，避开 C 盘）

**磁盘布局：**
| 盘 | 可用 | 用途 |
|----|------|------|
| C: | 125G | ❌ 系统盘，已排除大数据写入 |
| **D:** | **294G** | ✅ 项目代码、conda 环境、pip 缓存 |
| E: | 172G | 备用 |
| **G:** | **216G** | ✅ 模型/数据集/HF缓存/torch缓存 |

**已完成的缓存重定向（持久化到注册表 HKCU\Environment，对新开终端/IDE 生效）：**

| 环境变量 | 重定向到 | 作用 |
|----------|---------|------|
| `HF_HOME` | `G:\ProgramData\hello-agents-data\huggingface` | HuggingFace 主缓存（模型下载） |
| `HF_DATASETS_CACHE` | `G:\ProgramData\hello-agents-data\hf-datasets` | 数据集缓存（gsm8k 等） |
| `TRANSFORMERS_CACHE` | `G:\ProgramData\hello-agents-data\huggingface\transformers` | transformers 模型缓存 |
| `HUGGINGFACE_HUB_CACHE` | `G:\ProgramData\hello-agents-data\huggingface\hub` | HF Hub 模型缓存 |
| `TORCH_HOME` | `G:\ProgramData\hello-agents-data\torch` | PyTorch 模型缓存 |
| `HF_ENDPOINT` | `https://hf-mirror.com` | 国内 HF 镜像加速 |

**conda 环境目录：** 已设为 `D:\ProgramData\my_custom_envs` 优先（新环境自动建在 D 盘）

**pip 缓存：** 已在 `D:\Cache\pip`（阿里云源）

**已完成迁移：** C 盘旧 HF 缓存（783M）已迁移至 G 盘并删除原文件，C 盘已释放空间。

> ⚠️ 注意：以上环境变量通过 `setx` 写入注册表，**对新开的终端/IDE 生效**。当前已运行的终端需重启才能读到。验证命令：
> ```bash
> python -c "import os; print(os.environ.get('HF_HOME'))"  # 新终端应输出 G:\...
> ```

---

## 二、需要补充的项 🟡

| 项 | 动作 | 何时做 |
|---|------|--------|
| **API Keys** | 注册 AIHubmix（免费 GLM）+ Tavily，写入 `.env` | W1 开始前 |
| **`hello-agents` 框架** | `pip install hello-agents`（各章节版本不同，按需装） | Ch7 开始时 |
| **新建主学习环境** | `conda create -n hello-agents python=3.10` | W1 第一天 |
| **Ch6 框架** | autogen / agentscope / camel | Ch6 时按需装 |
| **Docker Desktop** | 学习 Ch5/8 前启动守护进程（装 Qdrant/Neo4j/n8n） | Ch5 前 |
| **Ollama**（可选） | Ch14 本地模型，可不装用云 API | Ch14 按需 |
| **Godot 4.5**（可选） | Ch15 仅体验，不强求开发 | Ch26 按需 |

---

## 三、主学习环境方案（已确认）

**决策**：新建专用 conda 环境 `hello-agents`，Python 3.10，作为全课程统一主环境。

**理由**：
- 隔离于 base（693 包，torch 是 CPU 版）和 tradingagents（已用于其他项目）
- Python 3.10 对齐项目要求（`hello-agents` 框架要求 3.10+）
- 训练章（Ch11）在同一环境内装 CUDA 版 torch，无需切换

**创建命令**（W1 第一天执行）：
```bash
# 1. 创建环境
conda create -n hello-agents python=3.10 -y
conda activate hello-agents

# 2. 装核心包（W1-W2 用）
pip install openai requests python-dotenv tavily-python jupyter pytest ruff

# 3. 装 CUDA 版 torch（Ch3 本地跑模型 + Ch11 训练用）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# 4. 验证 CUDA
python -c "import torch; print(torch.cuda.is_available())"  # 应输出 True

# 5. 后续按章节增量安装（hello-agents、transformers、fastapi 等）
```

---

## 四、各 conda 环境用途分工

| 环境 | Python | 用途 | torch |
|------|--------|------|-------|
| **hello-agents**（新建） | 3.10 | 🎯 **本项目主学习环境** | cu128（待装） |
| base (anaconda3) | 3.12 | 日常通用、已有 AI 包丰富 | cpu（勿用于训练） |
| py310 | 3.10 | 原有项目（torch+cu128 可临时借用作训练验证） | cu128 |
| tradingagents | 3.13 | 原有交易 Agent 项目 | - |
