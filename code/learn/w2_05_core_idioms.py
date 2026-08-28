"""
W2 主题5 练习: Agent 开发高频核心语法
=====================================
教学目标: 读 Ch7 框架源码 + Ch8 RAG 前, 必须熟练的 5 大语法
真实出处:
  - Ch7 my_simple_agent.py 的 Message.__repr__ / Agent.__call__
  - Ch8 检索结果的相似度排序 (sorted + lambda)
  - Ch7 tools 列表的推导式构建
  - Ch8 文档分块的生成器流式处理

★ 5 大核心 ★
  1. 推导式 (list/dict/set comprehension) — Java Stream.collect 的 Python 版
  2. 生成器 (yield) — 惰性求值, 处理大数据不爆内存
  3. 魔术方法 (__repr__/__call__/__getitem__ 等) — 运算符重载 + 协议
  4. lambda + 高阶函数 (sorted/map/filter) — Java Comparator/Stream API
  5. Enum 枚举 — Ch7 Message.role 的类型安全

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_05_core_idioms.py
"""
from enum import Enum, auto
from typing import List, Dict, Iterator


# ============================================================
# 第一部分: 推导式 (Java Stream 的 Python 版)
# ============================================================
print("=" * 60)
print("第一部分: 推导式 (comprehension)")
print("=" * 60)

# ★ Java 对照 ★
# Java: List<Integer> squares = nums.stream().map(n -> n*n).collect(toList());
# Py :  squares = [n*n for n in nums]                       # 更简洁!

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 1. 列表推导式
squares = [n * n for n in nums]
print(f"平方: {squares}")

# 2. 带过滤的推导式 (相当于 .filter().map())
evens = [n for n in nums if n % 2 == 0]
print(f"偶数: {evens}")

# 3. 带条件表达式 (相当于 ternary)
labels = ["偶" if n % 2 == 0 else "奇" for n in nums]
print(f"标签: {labels}")

# 4. 字典推导式 (Ch7 风格: 工具名 → 工具对象)
tool_names = ["calculator", "search", "weather"]
tool_dict = {name: f"<Tool {name}>" for name in tool_names}   ### 预测: 结构?
print(f"工具字典: {tool_dict}")

# 5. 集合推导式 (去重)
words = ["apple", "banana", "apple", "cherry", "banana"]
unique_first_letters = {w[0] for w in words}                  ### 预测: ? (去重!)
print(f"首字母集合: {unique_first_letters}")

# 6. 嵌套推导式 (谨慎用, 可读性差)
# Ch8 分块时偶用: 展平二维列表
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in nested for x in row]                     ### 预测: ?
print(f"展平: {flat}")
# 等价于:
# for row in nested:
#     for x in row:
#         ...  (顺序: 外层循环在前)

print("\n💡 推导式优先用, 比 for 循环 append 更 Pythonic")
print("   但嵌套超过 2 层就改用普通 for 循环, 别炫技")


# ============================================================
# 第二部分: 生成器 (yield) — 惰性求值
# ============================================================
print("\n" + "=" * 60)
print("第二部分: 生成器 (yield)")
print("=" * 60)

# ★ 核心区别 ★
# 列表推导式 [...]: 立刻算出全部, 占内存
# 生成器 (...):    惰性, 用一个算一个, 省内存

# 1. 生成器函数 (用 yield)
def count_up_to(n: int) -> Iterator[int]:
    """生成器: 每次调用 next() 吐一个值, 不一次性算完"""
    i = 0
    while i < n:
        yield i                                          # 暂停并返回 i
        i += 1                                           # 下次 next() 从这继续

gen = count_up_to(3)
print(f"生成器对象: {gen}")                               ### 预测: 不是列表!
print(f"第一个: {next(gen)}")                             ### 预测: ?
print(f"第二个: {next(gen)}")                             ### 预测: ?
print(f"第三个: {next(gen)}")                             ### 预测: ?
try:
    print(f"第四个: {next(gen)}")                         ### 预测: 抛啥异常?
except StopIteration:
    print(f"第四个: StopIteration (生成器耗尽)")

# 2. 生成器表达式 (类似列表推导式, 但用 ())
squares_list = [n * n for n in range(5)]                  # 列表: [0,1,4,9,16]
squares_gen = (n * n for n in range(5))                   # 生成器: 惰性
print(f"\n列表: {squares_list} (类型: {type(squares_list).__name__})")
print(f"生成器: {squares_gen} (类型: {type(squares_gen).__name__})")
# 生成器只能迭代一次! 迭代完就空了
print(f"生成器转列表: {list(squares_gen)}")
print(f"再转一次: {list(squares_gen)}")                   ### 预测: ? (空! 已耗尽)

# 3. Ch8 实战: 流式分块大文档 (不爆内存)
def chunk_text(text: str, chunk_size: int = 10) -> Iterator[str]:
    """生成器版分块: 逐块 yield, 适合大文件"""
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]

big_text = "abcdefghij" * 3                              # 假装是 30 字符的大文档
print(f"\n流式分块 (每次拿一块处理):")
for i, chunk in enumerate(chunk_text(big_text, chunk_size=10)):
    print(f"  块{i}: '{chunk}'")                          ### 预测: 3 块

# ★ Java 对照 ★
# Python yield ≈ Java Stream 的惰性特性, 但 Java 没有 yield 关键字
#           ≈ Java Iterator 的实现 (hasNext/next)
#           ≈ Kotlin/Rust 的 Sequence/Iterator yield


# ============================================================
# 第三部分: 魔术方法 (Dunder Methods)
# ============================================================
print("\n" + "=" * 60)
print("第三部分: 魔术方法 (__xxx__)")
print("=" * 60)

# 魔术方法 = Python 对象的"协议", 让自定义类支持内置操作

class Message:
    """Ch7 风格的消息类 (演示魔术方法)"""

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        """repr: 给开发者看 (调试/打印容器时显示)"""
        return f"Message(role='{self.role}', content='{self.content[:20]}')"

    def __str__(self) -> str:
        """str: 给用户看 (print 时显示)"""
        return f"[{self.role}] {self.content}"

    def __len__(self) -> int:
        """支持 len(msg)"""
        return len(self.content)

    def __eq__(self, other) -> bool:
        """支持 msg1 == msg2 (值相等)"""
        if not isinstance(other, Message):
            return NotImplemented
        return self.role == other.role and self.content == other.content

    def __getitem__(self, key):
        """支持 msg['role'] 字典式访问"""
        return getattr(self, key)


msg = Message("user", "你好, 请帮我规划北京三日游")

print(f"repr: {repr(msg)}")                              ### 预测: ?
print(f"str:  {msg}")                                    ### 预测: ? (print 调 __str__)
print(f"len:  {len(msg)}")                               ### 预测: ? (内容长度)
print(f"eq:   {msg == Message('user', '你好, 请帮我规划北京三日游')}")  ### True
print(f"getitem: {msg['role']}")                         ### 预测: ?

# ---- 最实用的魔术方法: __call__ (让对象像函数一样调用) ----
print("\n--- __call__: 让对象可调用 ---")

class Doubler:
    """实现 __call__ 后, 实例可以像函数一样用"""
    def __call__(self, x: int) -> int:
        return x * 2

d = Doubler()
print(f"d(5) = {d(5)}")                                  ### 预测: ? (对象当函数用!)
# Ch7 真实用法: LLM 客户端实例常做成 callable, agent.llm(prompt) 直接调用

# ---- 常用魔术方法速查 ----
print("""
魔术方法速查 (Ch7/Ch8 高频):
  __init__      构造 (new 对象时)
  __repr__      开发者字符串 (调试必用)
  __str__       用户字符串 (print 时)
  __len__       支持 len(obj)
  __eq__        支持 == (默认是比较内存地址!)
  __lt__/__gt__ 支持 < > (用于 sorted)
  __getitem__   支持 obj[key]
  __call__      支持 obj() (对象当函数用)
  __iter__      支持 for x in obj (迭代器协议)
  __enter__/__exit__  支持 with (w2_04 学过)
  __contains__  支持 in (x in obj)
""")


# ============================================================
# 第四部分: lambda + 高阶函数
# ============================================================
print("=" * 60)
print("第四部分: lambda + 高阶函数")
print("=" * 60)

# lambda = 匿名函数 (Java 的 (x) -> x*2)
# Java:  Comparator<Doc> byScore = (a, b) -> Double.compare(b.score, a.score);
# Py :   key=lambda d: d['score']

# 1. sorted 的 key (Ch8 检索结果按相似度排序, 最高频用法!)
docs = [
    {"text": "文档A", "score": 0.85},
    {"text": "文档B", "score": 0.92},
    {"text": "文档C", "score": 0.71},
    {"text": "文档D", "score": 0.88},
]
ranked = sorted(docs, key=lambda d: d["score"], reverse=True)   ### 预测: 顺序?
print("按分数降序:")
for d in ranked:
    print(f"  {d['text']}: {d['score']}")

# 2. min/max 也吃 key
best = max(docs, key=lambda d: d["score"])                     ### 预测: ?
print(f"最佳: {best['text']} ({best['score']})")

# 3. map (映射, Java Stream.map)
names = ["alice", "bob", "charlie"]
upper_names = list(map(str.capitalize, names))                 ### 预测: ?
print(f"map 首字母大写: {upper_names}")

# 4. filter (过滤, Java Stream.filter)
long_names = list(filter(lambda n: len(n) > 5, names))         ### 预测: ?
print(f"filter 长度>5: {long_names}")

# 5. 但! Python 更推荐用推导式替代 map/filter
upper_names2 = [n.capitalize() for n in names]                 # 比 map 更 Pythonic
long_names2 = [n for n in names if len(n) > 5]
print(f"推导式版: {upper_names2} / {long_names2}")

print("""
★ lambda 使用原则 ★
  1. 简单的一行用 lambda (sorted 的 key 最常见)
  2. 复杂逻辑用 def 命名函数 (可读性 > 简洁)
  3. map/filter 能用推导式替代就用推导式
  4. lambda 不能有语句 (只能单个表达式), 没有 return 关键字
""")


# ============================================================
# 第五部分: Enum 枚举 (Ch7 Message.role 的类型安全)
# ============================================================
print("=" * 60)
print("第五部分: Enum 枚举")
print("=" * 60)

# Java: enum Role { USER, ASSISTANT, SYSTEM, TOOL }
# Py :  class Role(Enum): USER = "user"; ...

class Role(Enum):
    """消息角色枚举 (Ch7 风格, 防止拼错字符串)"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

# 1. 访问
print(f"用户角色: {Role.USER}")                             ### 预测: ?
print(f"值: {Role.USER.value}")                            ### 预测: ? (小写 user)
print(f"名字: {Role.USER.name}")                           ### 预测: ? (大写 USER)

# 2. 用值反查
role_from_str = Role("assistant")                          ### 预测: ?
print(f"字符串转枚举: {role_from_str}")

# 3. 枚举的相等性和唯一性 (类型安全!)
print(f"USER == USER: {Role.USER == Role.USER}")           ### True
# Role.USER == "user"  # ❌ False! 枚举和字符串不相等 (这就是类型安全)
print(f"USER == 'user': {Role.USER == 'user'}")            ### 预测: ? (False!)

# 4. auto() 自动赋值 (不关心具体值时)
class Priority(Enum):
    LOW = auto()                                           # 自动 1, 2, 3
    MEDIUM = auto()
    HIGH = auto()

print(f"\n优先级: LOW={Priority.LOW.value}, MEDIUM={Priority.MEDIUM.value}, HIGH={Priority.HIGH.value}")

# 5. 遍历枚举 (Ch7 注册工具时偶用)
print("所有角色:")
for role in Role:
    print(f"  {role.name} = {role.value}")

print("""
★ Enum 的价值 ★
  1. 类型安全: Role.USER != "user" (避免字符串拼错 bug)
  2. IDE 补全: 输入 Role. 自动列出所有选项
  3. 可遍历: for role in Role
  4. 不可变: 枚举值运行时不能改

Ch7 中: 很多框架用 Literal["user","assistant"] 代替 Enum (更轻量)
        Enum 适合"有业务含义的固定集合" (角色/状态/级别)
""")


# ============================================================
# 第六部分: 综合实战 — Ch7 风格的工具注册表
# ============================================================
print("=" * 60)
print("第六部分: 综合实战 — 工具注册表 (Ch7 风格)")
print("=" * 60)

# 把 5 大语法揉在一起, 模拟 Ch7 的工具管理

class ToolRegistry:
    """工具注册表 (综合用推导式/生成器/魔术方法/lambda/Enum)"""

    def __init__(self):
        self._tools: Dict[str, dict] = {}

    def register(self, name: str, func, priority: int = 0):
        """注册工具"""
        self._tools[name] = {"func": func, "priority": priority}
        return func                                      # 返回原函数 (支持装饰器用法)

    def __call__(self, name: str, *args, **kwargs):
        """让注册表本身可调用: registry('name', args)"""
        if name not in self._tools:
            raise KeyError(f"工具 '{name}' 未注册")
        return self._tools[name]["func"](*args, **kwargs)

    def __contains__(self, name: str) -> bool:
        """支持 'name' in registry"""
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)

    def __repr__(self) -> str:
        names = list(self._tools.keys())
        return f"ToolRegistry({names})"

    def sorted_by_priority(self) -> List[str]:
        """按优先级排序返回工具名 (lambda + sorted)"""
        return [
            name for name, _ in sorted(
                self._tools.items(),
                key=lambda item: item[1]["priority"],
                reverse=True
            )
        ]

    def names_gen(self) -> Iterator[str]:
        """生成器: 逐个 yield 工具名"""
        for name in self._tools:
            yield name


# 使用
registry = ToolRegistry()

# 注册几个工具
registry.register("calculator", lambda expr: f"计算: {expr}", priority=2)
registry.register("search", lambda q: f"搜索: {q}", priority=1)
registry.register("weather", lambda city: f"天气: {city}", priority=3)

# 用魔术方法
print(f"repr: {registry}")                                ### 预测: ?
print(f"len: {len(registry)}")                            ### 预测: 3
print(f"'search' in registry: {'search' in registry}")    ### 预测: True
print(f"'translate' in registry: {'translate' in registry}")  ### False

# 用 __call__ 调用
print(f"\n调用 calculator: {registry('calculator', '2+3')}")  ### 预测: ?
print(f"调用 weather: {registry('weather', '北京')}")

# 按优先级排序 (lambda 大显身手)
print(f"\n按优先级排序: {registry.sorted_by_priority()}")     ### 预测: weather > calc > search

# 生成器遍历
print("工具列表 (生成器):")
for name in registry.names_gen():
    print(f"  - {name}")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("💡 核心语法速查 (Java 对照)")
print("=" * 60)
print("""
推导式:    [x for x in xs if cond]   ≡  Java Stream.filter().collect()
生成器:    (x for x in xs) / yield   ≡  Java Stream 惰性 / Iterator
魔术方法:  __repr__/__call__/__eq__   ≡  toString/对象()调用/equals
lambda:    sorted(xs, key=lambda..)  ≡  Comparator / Stream API
Enum:      class X(Enum): A="a"      ≡  enum X { A("a") }

★ Ch7 读源码前的 3 个必会 ★
  1. 看到类里有 __xxx__ 方法 → 想想它支持什么内置操作
  2. 看到 sorted(..., key=...) → lambda 提取排序键
  3. 看到 (x for x in ...) → 生成器, 惰性的, 只能迭代一次

这 5 个语法在 Ch7/Ch8/Ch11 几乎每个文件都出现, 务必熟练!
""")
