"""
W2 主题4-A 练习: async/await 异步编程 + dataclasses
=====================================================
教学目标: 能看懂 Ch13 FastAPI 的 async 路由 + Ch7 的数据类
真实出处: Ch13 trip.py 的 async def plan_trip + Ch7 的消息/配置数据

★ Java 程序员的核心认知转变 ★
  Java 异步: CompletableFuture / @Async / Reactor (多是线程池)
  Python 异步: asyncio (单线程事件循环, 类似 Node.js / Netty)

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_03_async_dataclass.py
"""
import asyncio
import time
from dataclasses import dataclass, field
from typing import List, Optional, Any


# ============================================================
# 第一部分: dataclasses (Java Record 的 Python 版)
# ============================================================
print("=" * 60)
print("第一部分: dataclasses (轻量数据类)")
print("=" * 60)

# dataclass = 自动生成 __init__/__repr__/__eq__ 的语法糖
# Java 类比: Java 14+ 的 record, 或 Lombok @Data
@dataclass
class Message:
    """OpenAI 消息格式 (Ch7 核心数据结构)"""
    role: str                                    # 必填
    content: str                                 # 必填
    tokens: int = 0                              # 有默认值

# 自动生成 __init__, 不用手写!
msg = Message(role="user", content="你好")        ### 预测: 能创建吗?
print(f"消息: {msg}")                             ### 预测: __repr__ 长啥样? (dataclass 自动生成)
print(f"角色: {msg.role}")                        ### 预测: ?

# 自动生成 __eq__ (值相等比较)
msg2 = Message(role="user", content="你好")
print(f"值相等: {msg == msg2}")                   ### 预测: ? (True/False)


# ---- dataclass vs pydantic BaseModel 的区别 ----
print("\n--- dataclass vs pydantic ---")
# dataclass: 轻量, 不校验类型, Python 标准库
# pydantic: 重量级, 运行时校验, 第三方库

@dataclass
class DataclassUser:
    name: str
    age: int

# dataclass 不校验类型! (和 pydantic 的核心区别)
u = DataclassUser(name=123, age="张三")           ### 会报错吗?
print(f"dataclass 不校验: name={u.name} (类型:{type(u.name).__name__})")   ### 预测: name 类型是啥?
# pydantic 会自动转成 str, dataclass 原样保留 int


# ---- dataclass 的高级用法 ----
print("\n--- dataclass 高级 ---")

@dataclass
class AgentConfig:
    """Agent 配置 (Ch7 风格)"""
    name: str
    model: str = "glm-4"                         # 默认值
    temperature: float = 0.7
    tools: List[str] = field(default_factory=list)  # 可变默认值用 field!
    metadata: dict = field(default_factory=dict)    # 可变默认值用 field!

config = AgentConfig(name="TravelBot")
print(f"配置: {config}")
print(f"工具: {config.tools}")                    ### 预测: ? (空列表)

# dataclass 的 frozen=True (不可变, 类似 Java String/record)
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p = ImmutablePoint(x=1.0, y=2.0)
try:
    p.x = 3.0                                    ### 能改吗?
except Exception as e:
    print(f"frozen 不可变: {type(e).__name__}")   ### 预测: 异常类型?


# ============================================================
# 第二部分: async/await 基础 (最反 Java 直觉的部分)
# ============================================================
print("\n" + "=" * 60)
print("第二部分: async/await 基础")
print("=" * 60)

# ★ 核心概念 ★
# async def 定义协程函数 (不是普通函数!)
# await 等待一个协程完成 (期间事件循环可以切走执行别的任务)
# asyncio.run() 启动事件循环

async def hello():
    """这是一个协程函数 (coroutine function)"""
    print("hello 开始")
    await asyncio.sleep(0.1)                     # 异步等待 (不阻塞线程!)
    print("hello 结束")
    return "done"

# 直接调用协程函数不会执行! (Java 程序员的大坑)
coro = hello()                                    ### 预测: 会打印 "hello 开始" 吗?
print(f"直接调用的返回: {type(coro).__name__}")    ### 预测: 返回啥? (不是 "done"!)
# coro 是个"协程对象", 还没跑! 必须被 await 或 asyncio.run 驱动
# 演示完关掉它, 否则 GC 前会触发 "coroutine was never awaited" 警告
coro.close()

# 必须用 asyncio.run() 才能真正执行
result = asyncio.run(hello())                     ### 预测: 现在会打印吗?
print(f"asyncio.run 返回: {result}")


# ============================================================
# 第三部分: 并发 vs 串行 (async 的核心价值)
# ============================================================
print("\n" + "=" * 60)
print("第三部分: 并发 vs 串行 (看时间差!)")
print("=" * 60)

async def call_llm(task_id: int, delay: float = 0.5):
    """模拟一次 LLM API 调用 (网络 IO)"""
    print(f"  [任务{task_id}] 开始调用...")
    await asyncio.sleep(delay)                   # 模拟网络等待 (非阻塞!)
    print(f"  [任务{task_id}] 完成")
    return f"任务{task_id}的结果"

async def serial_demo():
    """串行: 3 个任务依次执行"""
    start = time.time()
    r1 = await call_llm(1)
    r2 = await call_llm(2)
    r3 = await call_llm(3)
    elapsed = time.time() - start
    print(f"  串行耗时: {elapsed:.2f}s")          ### 预测: 约 ? 秒
    return [r1, r2, r3]

async def concurrent_demo():
    """并发: 3 个任务同时执行 (asyncio.gather)"""
    start = time.time()
    # asyncio.gather = 并发执行多个协程
    results = await asyncio.gather(
        call_llm(1),
        call_llm(2),
        call_llm(3)
    )
    elapsed = time.time() - start
    print(f"  并发耗时: {elapsed:.2f}s")          ### 预测: 约 ? 秒 (应该比串行快!)
    return results

print("--- 串行 ---")
asyncio.run(serial_demo())
print("\n--- 并发 ---")
asyncio.run(concurrent_demo())


# ============================================================
# 第四部分: 阻塞陷阱 (async 的最大坑!)
# ============================================================
print("\n" + "=" * 60)
print("第四部分: 阻塞陷阱 (★ 新手必踩 ★)")
print("=" * 60)

async def bad_async():
    """❌ 错误: 在 async 函数里用同步阻塞调用"""
    print("  bad: 开始")
    time.sleep(0.3)                              # ❌ 同步阻塞! 整个事件循环卡住!
    print("  bad: 结束")

async def good_async():
    """✅ 正确: 用 await 版本"""
    print("  good: 开始")
    await asyncio.sleep(0.3)                     # ✅ 异步等待
    print("  good: 结束")

# 规则: 在 async 函数里, 不能用 time.sleep / requests.get
# 要用 asyncio.sleep / httpx (async 版的 requests)
print("规则: async 函数里禁用同步阻塞 (time.sleep, requests.get)")
print("替代: asyncio.sleep, httpx.AsyncClient, aiofiles")


# ============================================================
# 第五部分: 实战 - 模拟 Ch13 FastAPI 异步路由
# ============================================================
print("\n" + "=" * 60)
print("第五部分: 实战 - 模拟 FastAPI 异步路由")
print("=" * 60)

# Ch13 的真实代码长这样 (trip.py):
#   @app.post("/api/trip/plan")
#   async def plan_trip(request: TripRequest):
#       result = await agent.run(request)
#       return result

async def mock_llm_call(prompt: str) -> str:
    """模拟 LLM 调用 (网络 IO)"""
    await asyncio.sleep(0.2)
    return f"回复: {prompt}"

async def mock_search(query: str) -> list:
    """模拟搜索调用 (网络 IO)"""
    await asyncio.sleep(0.3)
    return [f"{query}结果1", f"{query}结果2"]

# FastAPI 路由的典型模式
async def plan_trip(city: str):
    """Ch13 风格的异步路由处理"""
    print(f"  规划 {city} 行程...")

    # 并发调用 LLM + 搜索 (省时间!)
    llm_result, search_results = await asyncio.gather(
        mock_llm_call(f"规划{city}3天行程"),
        mock_search(f"{city}景点")
    )

    return {
        "city": city,
        "plan": llm_result,
        "attractions": search_results
    }

# 运行
start = time.time()
result = asyncio.run(plan_trip("北京"))
elapsed = time.time() - start
print(f"  结果: {result}")
print(f"  耗时: {elapsed:.2f}s")                   ### 预测: 0.3s 还是 0.5s? (并发!)


# ============================================================
# 第六部分: asyncio 常用 API 速查
# ============================================================
print("\n" + "=" * 60)
print("第六部分: asyncio 常用 API")
print("=" * 60)

async def api_demo():
    # 1. asyncio.gather - 并发执行多个
    results = await asyncio.gather(
        mock_llm_call("问题1"),
        mock_llm_call("问题2"),
        mock_llm_call("问题3")
    )
    print(f"  gather: {len(results)} 个结果")

    # 2. asyncio.wait_for - 超时控制
    try:
        result = await asyncio.wait_for(
            asyncio.sleep(2),
            timeout=0.1                          # 0.1秒超时
        )
    except asyncio.TimeoutError:
        print(f"  wait_for: 超时捕获 ✓")

    # 3. asyncio.create_task - 创建后台任务
    task = asyncio.create_task(mock_llm_call("后台任务"))
    # 做其他事...
    await asyncio.sleep(0.1)
    result = await task                          # 等待后台任务完成
    print(f"  create_task: {result[:15]}...")

asyncio.run(api_demo())


# ============================================================
# 第七部分: 同步代码调用异步 (常见场景)
# ============================================================
print("\n" + "=" * 60)
print("第七部分: 在同步代码里调异步 (Jupyter 常见坑)")
print("=" * 60)

# 场景: 你在 Jupyter/普通脚本里 (同步环境) 要调用 async 函数
# 方式1: asyncio.run() (推荐, 但不能嵌套)
result = asyncio.run(mock_llm_call("同步环境调用"))
print(f"  asyncio.run: {result[:15]}...")

# 方式2: Jupyter 里直接 await (Jupyter/IPython 自动有事件循环)
# 在 .py 文件里不行, 在 .ipynb 里可以:
#   result = await mock_llm_call("xxx")  # Jupyter 里直接写

print("  Jupyter 笔记本里可以直接写 await xxx (不需要 asyncio.run)")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("💡 async/dataclass 核心速查 (Java 对照)")
print("=" * 60)
print("""
dataclass:
  = Java Record / Lombok @Data (轻量数据类)
  @dataclass 自动生成 __init__/__repr__/__eq__
  field(default_factory=list) 处理可变默认值
  frozen=True 不可变
  vs pydantic: dataclass 不校验类型, pydantic 校验

async/await:
  = Node.js / Netty 的单线程事件循环 (不是多线程!)
  async def 定义协程函数
  await 等待协程 (期间可切换到其他任务)
  asyncio.run(main()) 启动
  asyncio.gather(*tasks) 并发执行

★ 三大铁律 ★
  1. 协程函数直接调用不执行! 必须 await 或 asyncio.run
  2. async 函数里禁用同步阻塞 (time.sleep/requests)
     用 asyncio.sleep / httpx 替代
  3. 并发用 asyncio.gather, 不是多线程

Ch13 FastAPI 的所有路由都是 async def (你第4周会写)
""")
