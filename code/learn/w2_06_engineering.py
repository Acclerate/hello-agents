"""
W2 主题6 练习: 工程化补充语法
=============================
教学目标: Ch8 文档加载 / Ch11 数据缓存 / Ch7 配置合并会用到的工程化语法
真实出处:
  - Ch8 RAG 加载 docs/ 下所有 .md (pathlib)
  - Ch11 缓存 embedding 向量 (functools.lru_cache)
  - Ch7 多 provider 默认参数合并 (字典解包)

★ 3 大工程化利器 ★
  1. pathlib — 现代路径操作 (替代 os.path, 面向对象)
  2. functools — @lru_cache(缓存) / partial(偏函数) / reduce
  3. 解包进阶 — **dict 合并 / *拆解 / | 运算符 (3.9+)

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_06_engineering.py
"""
import os
from pathlib import Path
from functools import lru_cache, partial, reduce
from typing import Dict, Any


# ============================================================
# 第一部分: pathlib (现代路径操作)
# ============================================================
print("=" * 60)
print("第一部分: pathlib (替代 os.path)")
print("=" * 60)

# ★ Java 对照 ★
# Java: Path p = Paths.get("a", "b", "c.txt");  Files.exists(p);
# Py :  p = Path("a") / "b" / "c.txt";          p.exists()

# 1. 创建 Path 对象
p1 = Path("code") / "learn" / "w2_06_engineering.py"       # 用 / 拼接! (魔术方法)
p2 = Path("code/learn") / "w2_06_engineering.py"
print(f"路径1: {p1}")
print(f"路径2: {p2}")
print(f"相等: {p1 == p2}")                                 ### 预测: ? (值相等)

# 2. 路径组件 (Ch8 加载文档时常用)
current_file = Path(__file__)                              # 本文件的绝对路径
print(f"\n当前文件:")
print(f"  绝对路径: {current_file.resolve()}")
print(f"  父目录: {current_file.parent}")                  ### 预测: code/learn
print(f"  文件名: {current_file.name}")                    ### w2_06_engineering.py
print(f"  文件名(无后缀): {current_file.stem}")            ### 预测: ?
print(f"  后缀: {current_file.suffix}")                    ### 预测: ? (.py)

# 3. 常用操作
print(f"\n  存在: {current_file.exists()}")                ### True
print(f"  是文件: {current_file.is_file()}")               ### True
print(f"  是目录: {current_file.is_dir()}")                ### False

# 4. 遍历目录 (Ch8 加载 docs/ 的真实用法)
print(f"\n当前目录下的 .py 文件 (glob):")
learn_dir = current_file.parent
for py_file in sorted(learn_dir.glob("w2_*.py")):          ### 预测: 列出哪些?
    print(f"  {py_file.name}")

# 5. 读写文件 (Ch8/Ch9 文档处理首选 pathlib)
# Path 对象直接有 read_text/write_text 方法
demo_file = learn_dir / "_pathlib_demo.txt"
demo_file.write_text("hello pathlib 中文", encoding="utf-8")
content = demo_file.read_text(encoding="utf-8")
print(f"\n读写测试: '{content}'")
demo_file.unlink()                                        # 删除文件

print("""
★ pathlib vs os.path ★
  os.path.join("a","b")     →  Path("a") / "b"        (更优雅)
  os.path.exists(p)         →  Path(p).exists()
  os.path.dirname(p)        →  Path(p).parent
  os.path.basename(p)       →  Path(p).name
  open(p)                   →  Path(p).read_text()
  glob.glob("*.py")         →  Path(".").glob("*.py")
  ★ 新代码统一用 pathlib, os.path 是老代码遗留
""")


# ============================================================
# 第二部分: functools — @lru_cache (缓存)
# ============================================================
print("=" * 60)
print("第二部分: functools — @lru_cache (Ch11 embedding 缓存)")
print("=" * 60)

# @lru_cache = 自动缓存函数结果 (相同入参直接返回, 不重算)
# Java 类比: Guava CacheBuilder / Caffeine / @Cacheable

call_count = 0

@lru_cache(maxsize=128)                                    # 缓存最近 128 次调用
def fake_embed(text: str) -> tuple:
    """模拟 embedding (Ch8 真实场景: 调 API 把文本转向量)"""
    global call_count
    call_count += 1
    # 假装做了昂贵的计算 (实际是调 API)
    return tuple(ord(c) for c in text[:5])                # 返回 tuple (不可变, 可哈希)

# 第一次调用 (真正计算)
r1 = fake_embed("hello")
print(f"第1次调用, 计数={call_count}")                     ### 预测: 1

# 第二次相同入参 (命中缓存, 不计算!)
r2 = fake_embed("hello")
print(f"第2次调用, 计数={call_count}")                     ### 预测: ? (还是 1! 缓存命中)
print(f"结果相同: {r1 == r2}")

# 不同入参 (重新计算)
r3 = fake_embed("world")
print(f"第3次调用(不同入参), 计数={call_count}")           ### 预测: 2

# 查看缓存信息
print(f"\n缓存信息: {fake_embed.cache_info()}")
# CacheInfo(hits=1, misses=2, maxsize=128, currsize=2)

# 清缓存
fake_embed.cache_clear()
print(f"清空后: {fake_embed.cache_info()}")

print("""
★ @lru_cache 的坑 ★
  1. 入参必须可哈希 (list/dict/set 不行! 要传 tuple/frozenset)
  2. 缓存的是返回值, 如果返回可变对象, 外部修改会污染缓存
  3. maxsize=None 表示无限制 (慎用, 内存会爆)

Ch11 用途: embedding 向量缓存 (同一文本不重复调 API, 省钱!)
""")


# ============================================================
# 第三部分: functools — partial (偏函数)
# ============================================================
print("\n" + "=" * 60)
print("第三部分: functools — partial (固定部分参数)")
print("=" * 60)

# partial = 把一个函数的某些参数固定, 生成新函数
# Java: 没有直接对应, 类似 MethodHandle.bindTo

def make_llm_call(model: str, temperature: float, prompt: str) -> str:
    """模拟 LLM 调用 (3 个参数)"""
    return f"[{model}@{temperature}] {prompt}"

# 固定 model 和 temperature, 只留 prompt
# Ch7 真实用法: 一个 provider 对应一组默认参数
glm4_call = partial(make_llm_call, "glm-4", 0.7)          # 固定前两个参数
deepseek_call = partial(make_llm_call, "deepseek-chat", 0.3)

print(f"glm4: {glm4_call('你好')}")                       ### 预测: ?
print(f"deepseek: {deepseek_call('你好')}")               ### 预测: ? (不同模型!)

# partial 还能继续叠加
glm4_creative = partial(glm4_call, temperature=0.9)        # 不对! 已固定的不能改
# 上面的写法会报错或无效, partial 只能固定"未固定"的参数
# 正确做法是直接基于原函数
print(f"创意模式: {partial(make_llm_call, 'glm-4')(0.9, '写诗')}")


# ============================================================
# 第四部分: functools — reduce (累积)
# ============================================================
print("\n" + "=" * 60)
print("第四部分: functools — reduce")
print("=" * 60)

# reduce = 把列表逐个累积成一个值
# Java: stream.reduce((a, b) -> a + b)

nums = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, nums)                   ### 预测: 15
print(f"求和: {total}")

# 累积过程: ((((1+2)+3)+4)+5) = 15
# 带初始值
total_with_init = reduce(lambda a, b: a + b, nums, 100)    ### 预测: ?
print(f"带初始值100: {total_with_init}")

# 求最大值 (虽然 max() 更好)
maximum = reduce(lambda a, b: a if a > b else b, nums)
print(f"最大值: {maximum}")

print("💡 简单场景有内置函数 (sum/max/min), reduce 适合复杂累积逻辑")


# ============================================================
# 第五部分: 解包进阶 (**dict / *list)
# ============================================================
print("\n" + "=" * 60)
print("第五部分: 解包进阶 (Ch7 配置合并)")
print("=" * 60)

# 1. **dict 解包: 合并字典 (Ch7 多 provider 默认参数)
default_config = {"model": "glm-4", "temperature": 0.7, "max_tokens": 1000}
user_config = {"temperature": 0.3, "top_p": 0.9}          # 用户想覆盖的

# 方式A: ** 解包 (3.5+)
merged = {**default_config, **user_config}                 ### 预测: ? (后者覆盖前者)
print(f"合并 (**): {merged}")

# 方式B: | 运算符 (3.9+, 更直观)
merged2 = default_config | user_config                     ### 预测: ?
print(f"合并 (|):  {merged2}")

# 就地合并 (3.9+)
config = {"a": 1}
config |= {"b": 2, "a": 99}                                ### 预测: ?
print(f"就地合并 (|=): {config}")

# 2. **dict 传函数参数 (Ch7 框架内部常见)
def create_agent(name: str, model: str, **kwargs):
    """**kwargs 收集额外参数为字典"""
    print(f"  创建 {name}, model={model}, 额外: {kwargs}")

agent_kwargs = {"temperature": 0.5, "tools": ["search"], "verbose": True}
create_agent("Bot", model="glm-4", **agent_kwargs)         ### ** 解包字典为关键字参数

# 3. *list 解包: 函数位置参数
def add4(a, b, c, d):
    return a + b + c + d

args = [1, 2, 3, 4]
print(f"\n*解包: add4(*args) = {add4(*args)}")             ### 预测: 10

# 4. 解包合并列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2, 7]                              ### 预测: ?
print(f"列表合并: {combined}")

# 5. 高级: 同时用 * 和 **
def show(*args, **kwargs):
    print(f"  args = {args}")      # tuple
    print(f"  kwargs = {kwargs}")  # dict

show(1, 2, 3, name="x", age=20)                           # 混合接收

print("""
★ 解包速记 ★
  *xs    → 列表/元组解包 (位置参数)
  **d    → 字典解包 (关键字参数)
  {**a, **b}  → 合并字典 (b 覆盖 a)
  a | b       → 3.9+ 字典合并 (更直观)
  [*a, *b]    → 列表合并
""")


# ============================================================
# 第六部分: 实战 — Ch8 风格的文档加载器
# ============================================================
print("=" * 60)
print("第六部分: 实战 — Ch8 文档加载器 (综合)")
print("=" * 60)

@lru_cache(maxsize=32)
def load_and_count(file_path: str) -> Dict[str, Any]:
    """加载文档并统计 (带缓存, 同一文件不重复读)"""
    p = Path(file_path)
    if not p.exists():
        return {"error": f"{file_path} 不存在"}
    text = p.read_text(encoding="utf-8")
    return {
        "path": str(p),
        "chars": len(text),
        "lines": text.count("\n") + 1,
    }

# 加载本文件自己
stats = load_and_count(__file__)
print(f"本文件统计: {stats}")

# 再加载一次 (命中缓存)
load_and_count(__file__)
print(f"缓存信息: {load_and_count.cache_info()}")         ### 预测: hits=1

# 配置合并示例 (pathlib + 解包)
base = {"chunk_size": 500, "overlap": 50, "encoding": "utf-8"}
user_override = {"chunk_size": 300}
final_config = base | user_override
print(f"\nRAG 配置 (合并): {final_config}")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("💡 工程化语法速查 (Java 对照)")
print("=" * 60)
print("""
pathlib:    Path("a") / "b.txt"     ≡  Java NIO Path/Files
lru_cache:  @lru_cache(maxsize=N)   ≡  Guava/Caffeine @Cacheable
partial:    partial(f, 固定参数)     ≡  绑定部分参数生成新函数
reduce:     reduce(f, xs)           ≡  stream.reduce(...)
**dict:     {**a, **b}              ≡  Map.putAll (b 覆盖 a)
| 运算符:   a | b                   ≡  同上 (3.9+, 更直观)

★ 工程化原则 ★
  1. 路径操作统一用 pathlib (新代码别用 os.path)
  2. 昂贵且纯的函数加 @lru_cache (embedding, 解析结果)
  3. 字典合并用 | 运算符 (3.9+), 老代码用 {**a, **b}
  4. 解包传参让代码更声明式 (**kwargs 透传)
""")
