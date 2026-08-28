"""
W2 主题7 练习: 现代 Python 语法 (了解即可)
=========================================
教学目标: 看到这些语法能读懂, 不强制掌握
真实出处: Ch11 训练脚本偶用 __slots__/itertools, 流式处理见 walrus

★ 4 个现代语法 (按使用频率排序) ★
  1. walrus operator := (3.8+) — 赋值表达式, 流式读取常见
  2. match-case (3.10+) — 结构化模式匹配, 比 if-elif 清晰
  3. __slots__ — 大量对象的内存优化 (Ch11 数据类)
  4. itertools — 批处理迭代工具集

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_07_modern.py
"""
import sys
import itertools
from typing import List


# ============================================================
# 第一部分: walrus operator := (海象运算符)
# ============================================================
print("=" * 60)
print("第一部分: walrus operator := (3.8+)")
print("=" * 60)

# := 是"赋值表达式", 在表达式内部赋值
# 解决痛点: 避免"先赋值再判断"两步走

# 1. 经典场景: while 读输入 (避免重复调用)
print("--- 经典场景: while 循环 ---")
# 没用 walrus (啰嗦):
#   chunk = read_chunk()
#   while chunk:
#       process(chunk)
#       chunk = read_chunk()  ← 又调一次

# 用 walrus (简洁):
chunks = ["data1", "data2", "", "data4"]                   # 模拟流 (空字符串=结束)
idx = 0
def next_chunk():
    global idx
    if idx < len(chunks):
        c = chunks[idx]
        idx += 1
        return c
    return ""

# walrus 版: while (chunk := next_chunk()):  (一行搞定)
processed = []
while (chunk := next_chunk()):                             ### 预测: 处理几个?
    processed.append(chunk)
print(f"处理的块: {processed}")                            ### 预测: ['data1','data2'] (空串停止)

# 2. 场景: 列表推导式里复用计算结果
print("\n--- 推导式里复用计算 ---")
texts = ["hello", "hi", "greetings", "hey"]
# 不用 walrus: 要算两次 len
# longs = [t for t in texts if len(t) > 3]
#         [f"{t}({len(t)})" for t in texts if len(t) > 3]  ← len 重复算

# 用 walrus: 算一次, 复用
# (n := len(t)) 把长度赋给 n, 同时返回 n 用于条件判断
result = [f"{t}({n})" for t in texts if (n := len(t)) > 3]  ### 预测: ?
print(f"长文本: {result}")                                 ### 预测: ['hello(5)', 'greetings(9)']

# 3. 场景: if 条件里赋值
print("\n--- if 条件赋值 ---")
config = {"api_key": "sk-xxx"}
if (key := config.get("api_key")):                         ### 预测: key 有值吗?
    print(f"找到 key: {key[:5]}...")                       ### 会执行
else:
    print("无 key")

print("""
★ walrus 使用原则 ★
  1. 当一个计算结果既要"判断"又要"使用"时用 := 最爽
  2. 别滥用! 简单场景用普通赋值更清晰
  3. 读老代码看到 := 别懵, 就是"边赋值边判断"
""")


# ============================================================
# 第二部分: match-case (3.10+ 结构化模式匹配)
# ============================================================
print("\n" + "=" * 60)
print("第二部分: match-case (3.10+)")
print("=" * 60)

# ★ Java 对照 ★
# Java 17+: switch (x) { case "a" -> ...; case "b" -> ...; }
# Py 3.10+: match x: case "a": ...; case "b": ...

# 检查版本 (3.10+ 才支持)
if sys.version_info < (3, 10):
    print("⚠️ 当前 Python < 3.10, 跳过 match-case 演示 (用 if-elif 替代)")
    print("   match-case 本质是增强版 switch, 支持解构和模式匹配")
else:
    # 1. 基础: 类似 switch
    def handle_role(role: str) -> str:
        match role:
            case "user":
                return "用户消息"
            case "assistant":
                return "助手回复"
            case "system":
                return "系统指令"
            case _:                                      # _ 是通配 (default)
                return f"未知角色: {role}"

    print(f"user → {handle_role('user')}")                ### 预测: ?
    print(f"tool → {handle_role('tool')}")                ### 预测: 未知角色

    # 2. 解构匹配 (比 if-elif 强大之处)
    def parse_command(cmd):
        match cmd:
            case {"action": "search", "query": q}:
                return f"搜索: {q}"
            case {"action": "calc", "expr": e}:
                return f"计算: {e}"
            case {"action": "exit"}:
                return "退出"
            case _:
                return "无法解析"

    print(f"\n{parse_command({'action': 'search', 'query': '天气'})}")  ### 预测: ?
    print(f"{parse_command({'action': 'exit'})}")          ### 预测: 退出

    # 3. 列表解构
    def handle_args(args):
        match args:
            case []:
                return "无参数"
            case [single]:
                return f"单参数: {single}"
            case [first, second]:
                return f"双参数: {first}, {second}"
            case [first, *rest]:                          # *rest 收集剩余
                return f"首参: {first}, 其余 {len(rest)} 个"

    print(f"\n{handle_args([])}")                         ### 无参数
    print(f"{handle_args(['a'])}")                        ### 单参数
    print(f"{handle_args(['a', 'b', 'c', 'd'])}")         ### 预测: 首参 a, 其余 3 个

print("""
★ match-case 原则 ★
  1. 多分支 + 需要解构时, 比 if-elif 清晰得多
  2. _ 是通配符 (必须放最后), 相当于 switch 的 default
  3. Python 3.10+ 才支持, 老项目可能用 if-elif
  4. Ch7 框架源码目前多用 if-elif (兼容性考虑)
""")


# ============================================================
# 第三部分: __slots__ (内存优化)
# ============================================================
print("\n" + "=" * 60)
print("第三部分: __slots__ (Ch11 数据类内存优化)")
print("=" * 60)

# 默认: Python 对象用 __dict__ 存属性 (灵活但费内存)
# __slots__: 固定属性列表, 省内存 (Ch11 训练时几百万对象时关键)

# 1. 普通类 (有 __dict__)
class NormalMessage:
    def __init__(self, role, content):
        self.role = role
        self.content = content

# 2. slots 类 (无 __dict__, 省内存)
class SlotMessage:
    __slots__ = ("role", "content")                        # 声明固定属性
    def __init__(self, role, content):
        self.role = role
        self.content = content

m1 = NormalMessage("user", "hi")
m2 = SlotMessage("user", "hi")

# 功能一样
print(f"普通: {m1.role}, {m1.content}")
print(f"slots: {m2.role}, {m2.content}")

# 区别1: slots 不能加新属性
try:
    m2.new_attr = "x"                                      ### 预测: 能加吗?
except AttributeError as e:
    print(f"slots 不能加新属性: {e}")

m1.new_attr = "x"                                          # 普通类能加
print(f"普通类能加属性: {m1.new_attr}")

# 区别2: slots 没有 __dict__
print(f"\n普通类 __dict__: {m1.__dict__}")                 ### 预测: 有
print(f"slots 类有 __dict__? {hasattr(m2, '__dict__')}")   ### 预测: False

# 内存对比 (粗略)
import sys
print(f"\n普通对象大小: {sys.getsizeof(m1.__dict__)} bytes (dict)")
print(f"slots 对象: 无 __dict__, 省下这部分内存")

print("""
★ __slots__ 原则 ★
  1. 大量同类对象 (如 Ch11 训练数据几百万条) 时用, 省 40-50% 内存
  2. 代价: 不能动态加属性, 失去灵活性
  3. 一般业务代码不用, 数据密集型场景才上
  4. 读源码看到 __slots__ 就知道: 这是为内存优化的
""")


# ============================================================
# 第四部分: itertools (批处理工具集)
# ============================================================
print("\n" + "=" * 60)
print("第四部分: itertools (批处理利器)")
print("=" * 60)

# Java 对照: Stream API / Guava Iterables

# 1. chain — 串联多个迭代器
list1 = [1, 2, 3]
list2 = [4, 5, 6]
chained = list(itertools.chain(list1, list2))              ### 预测: ?
print(f"chain: {chained}")

# 2. islice — 切片迭代器 (流式取前 N 个)
stream = range(100)
first5 = list(itertools.islice(stream, 5))                 ### 预测: ?
print(f"islice 前5: {first5}")

# 3. batched (3.12+, 批处理) — Ch11 数据加载的神器
# Ch11 训练时: 把 1000 条数据按 batch_size=32 分批
if sys.version_info >= (3, 12):
    data = list(range(10))
    batches = list(itertools.batched(data, 3))             ### 预测: 几批?
    print(f"batched(3): {batches}")                        ### [(0,1,2),(3,4,5),(6,7,8),(9,)]
else:
    print(f"batched 需 3.12+, 当前 {sys.version_info.major}.{sys.version_info.minor}, 手动实现")
    # 手动 batch (兼容写法, Ch11 常见)
    def batched(iterable, n):
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):     # walrus + islice!
            yield batch
    data = list(range(10))
    batches = list(batched(data, 3))                       ### 预测: ?
    print(f"手动 batched(3): {batches}")

# 4. groupby — 分组 (注意: 要先排序!)
data = [("a", 1), ("a", 2), ("b", 3), ("a", 4)]
data_sorted = sorted(data, key=lambda x: x[0])             # groupby 要求先排序!
for key, group in itertools.groupby(data_sorted, key=lambda x: x[0]):
    print(f"  组 {key}: {list(group)}")

# 5. product — 笛卡尔积 (Ch11 超参搜索偶用)
for model, lr in itertools.product(["glm-4", "qwen"], [1e-4, 5e-5]):
    print(f"  组合: {model} + lr={lr}")

print("""
★ itertools 原则 ★
  1. 都是"惰性"的 (返回迭代器, 要 list() 才算完)
  2. chain/islice 最常用, batched 是 3.12 新增 (训练神器)
  3. groupby 必须先排序! (新手大坑)
  4. 读源码遇到 itertools.xxx, 想想 Java Stream API 对应方法
""")


# ============================================================
# 第五部分: 实战 — 综合用例
# ============================================================
print("\n" + "=" * 60)
print("第五部分: 综合 — 流式分块 + 批处理")
print("=" * 60)

# 模拟 Ch11 数据加载: 流式读 + 批处理 (现代语法全用上)

def stream_records(total: int):
    """生成器: 流式产生记录"""
    for i in range(total):
        yield {"id": i, "text": f"记录{i}"}

# 用 walrus 在 while 里流式取批
def load_batches(records, batch_size=4):
    """流式分批 (不用一次性加载全部到内存)"""
    it = iter(records)
    batch_num = 0
    # walrus + islice: 一行搞定流式取批
    while batch := list(itertools.islice(it, batch_size)):
        batch_num += 1
        print(f"  批{batch_num}: {[r['id'] for r in batch]}")
        if batch_num >= 3:                                 # 演示, 只取 3 批
            break

print("流式分批加载:")
load_batches(stream_records(100), batch_size=4)

# match-case 处理不同消息类型 (3.10+)
if sys.version_info >= (3, 10):
    print("\n消息分发:")
    messages = [
        {"type": "text", "content": "你好"},
        {"type": "image", "url": "http://..."},
        {"type": "tool_call", "name": "search"},
    ]
    for msg in messages:
        match msg:
            case {"type": "text", "content": c}:
                print(f"  文本: {c[:10]}")
            case {"type": "image", "url": u}:
                print(f"  图片: {u[:15]}...")
            case {"type": "tool_call", "name": n}:
                print(f"  工具调用: {n}")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("💡 现代语法速查 (Java 对照)")
print("=" * 60)
print("""
walrus :=      边赋值边判断        ≡  Java 无直接对应 (语法糖)
match-case     结构化模式匹配       ≡  Java 17+ switch 表达式 + 解构
__slots__      固定属性省内存       ≡  Java final 字段 + 无反射
itertools      批处理工具集         ≡  Java Stream API / Guava

★ 现代语法原则 ★
  1. 看到 := 别懵 — 是"赋值+返回"的二合一
  2. 看到 match-case — 当作增强版 switch
  3. 看到 __slots__ — 知道是为省内存 (大量对象场景)
  4. 看到 itertools — 想想 Java Stream API

这些语法"能读懂"即可, 写代码优先用前面 w2_01-06 的基础语法!
Python 语法阶段真正全部结束了, 可以放心进 Ch1 理论 🎉
""")
