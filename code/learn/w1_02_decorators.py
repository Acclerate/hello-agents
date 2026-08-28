"""
W1 主题2-A 练习：装饰器 (Decorator)
=====================================
教学目标: 理解装饰器本质，能看懂 Ch7 框架里的装饰器代码
学习方法: 和 w1_01 一样，先预测 ### 处的输出，再运行对照

运行方式:
cd D:\\privategit\\github\\Hello-Agents\\code\\learn
D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w1_02_decorators.py

★ 重要提醒 ★
Java 的 @Override 是"标记注解"(不改行为)
Python 的 @decorator 是"代码变换"(真改变行为) —— 这是最大思维转变!
"""

import time
import functools


# ============================================================
# 第 0 层: 函数是一等公民 (装饰器的前提)
# ============================================================
print("=" * 60)
print("第 0 层: 函数可以像变量一样传递 (Java 做不到)")
print("=" * 60)

def greet(name):
    return f"Hello, {name}"

# 1. 函数赋值给变量 (Java 8 之前做不到)
say_hi = greet                          # 注意没有括号! greet 是函数本身
print(say_hi("北京"))                    ### 预测: 北京× 实际是 Hello, 北京

# 2. 函数作为参数传递 (对应 Java 8 Lambda::method)
def apply_twice(func, value):
    return func(func(value))             # 把函数当参数用
print(apply_twice(greet, "World"))       ### 预测: World 实际是 Hello, Hello, World


# ============================================================
# 第 1 层: 手写一个装饰器 (理解原理)
# ============================================================
print("\n" + "=" * 60)
print("第 1 层: 手写装饰器 (不用 @ 语法)")
print("=" * 60)

# 装饰器本质: 一个"接收函数, 返回新函数"的函数
def add_log(func):
    def wrapper(*args, **kwargs):        # *args/**kwargs 后面解释
        print(f"  [LOG] 开始调用 {func.__name__}")
        result = func(*args, **kwargs)   # 原样转发所有参数
        print(f"  [LOG] 调用完成, 返回: {result}")
        return result
    return wrapper                        # 注意: 返回函数本身, 不是调用

# 手动装饰 (不用 @)
def get_weather(city):
    return f"{city}: 晴朗"

get_weather_logged = add_log(get_weather)  # 手动包装
print(get_weather_logged("上海"))            ### 预测: 打印几行?3  1 [LOG] 开始调用 get_weather   2 [LOG] 调用完成, 返回: 上海: 晴朗 3 上海: 晴朗



# ============================================================
# 第 2 层: @ 语法糖 (和第 1 层完全等价!)
# ============================================================
print("\n" + "=" * 60)
print("第 2 层: @ 语法糖 (这就是你以后最常见的写法)")
print("=" * 60)

# 下面这两段代码完全等价:
#
#   @add_log
#   def f(): ...
#
# 等价于:
#
#   def f(): ...
#   f = add_log(f)
#
# @add_log 只是上面第二行的语法糖!

@add_log                                  # ← 这一行就是魔法
def get_temperature(city):
    return f"{city}: 30℃"

print(get_temperature("深圳"))             ### 预测: 打印几行?


# ============================================================
# 第 3 层: 实战装饰器 (Ch7/Ch4 框架真实场景)
# ============================================================
print("\n" + "=" * 60)
print("第 3 层: 4 个实战装饰器 (本书/工业代码常用)")
print("=" * 60)

# === 实战 1: 计时装饰器 ===
# 场景: 测量 LLM API 调用耗时 (Ch4 你会用到)
def timer(func):
    @functools.wraps(func)                # 保留原函数名 (不然会被改成 wrapper)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  ⏱ {func.__name__} 耗时 {elapsed:.4f}秒")
        return result
    return wrapper

@timer
def slow_llm_call(query):
    """模拟一次慢速 LLM 调用"""
    time.sleep(0.5)                       # 模拟网络延迟
    return f"回复: {query}"

print("--- 计时装饰器 ---")
result = slow_llm_call("天气如何")          ### 预测: 会显示多少秒?
print(f"  结果: {result}")
print(f"  函数名仍是: {slow_llm_call.__name__}")  ### 预测: ? (functools.wraps 的作用)


# === 实战 2: 带参数的装饰器 (三层嵌套, 最难但最实用) ===
# 场景: Ch7 工具注册时指定工具名/描述
print("\n--- 带参数的装饰器 ---")

def register_tool(name: str, description: str = ""):
    # 注意: 带参数的装饰器要多一层嵌套!
    def decorator(func):
        # 用一个全局字典模拟工具注册表 (Ch7 框架就是这么做的)
        TOOL_REGISTRY[name] = {
            "func": func,
            "description": description or func.__doc__ or ""
        }
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

TOOL_REGISTRY = {}                        # 工具注册表 (全局)

@register_tool("weather", "查询城市天气")   # 带参数的装饰器!
def get_weather(city: str) -> str:
    """天气工具"""
    return f"{city}: 晴"

@register_tool("calc", "计算器")
def calculate(expression: str) -> str:
    """计算工具"""
    return f"结果: {expression}"

print(f"已注册工具: {list(TOOL_REGISTRY.keys())}")  ### 预测: ?
print(f"weather 工具描述: {TOOL_REGISTRY['weather']['description']}")
# 这就是 Ch7 框架注册工具的核心机制!


# ============================================================
# 第 4 层: 内置装饰器 (你每天都会用)
# ============================================================
print("\n" + "=" * 60)
print("第 4 层: Python 内置装饰器 (这些你以后天天见)")
print("=" * 60)

# === @staticmethod: 类的静态方法 (和 Java 一模一样!) ===
class MathHelper:
    @staticmethod                          # 等价 Java: public static int add(...)
    def add(a, b):
        return a + b

    @classmethod                           # 等价 Java: 工厂方法
    def create_default(cls):
        return cls()                       # cls = 类本身 (类似 Java 的 new ClassName())

# 不需要实例化就能调用静态方法 (和 Java 一样!)
print(f"3 + 5 = {MathHelper.add(3, 5)}")   ### 预测: ?

# === @property: 把方法变成属性访问 (Java 程序员要重点理解) ===
# 场景: Ch7 的 Config 类大量使用
class LLMConfig:
    def __init__(self, model: str):
        self._model = model                # 下划线开头 = 约定的"私有"

    @property                              # 读: config.model (不加括号)
    def model(self):
        return self._model

    @model.setter                          # 写: config.model = "xxx"
    def model(self, value):
        if not value:
            raise ValueError("model 不能为空")
        self._model = value

config = LLMConfig("glm-4")
print(f"模型: {config.model}")             ### 预测: ? (注意: 没有 () 括号!)
config.model = "deepseek-v3"               # 像属性一样赋值 (实际调用 setter)
print(f"改后: {config.model}")             ### 预测: ?


# ============================================================
# 总结: 装饰器记忆口诀
# ============================================================
print("\n" + "=" * 60)
print("💡 装饰器记忆口诀")
print("=" * 60)
print("""
1. 装饰器 = "接收函数 → 返回新函数" 的函数
2. @add_log 就是 f = add_log(f) 的语法糖
3. @staticmethod / @property / @classmethod 是内置三大件
4. 带参数的装饰器要多嵌套一层 (三层)
5. 永远加 @functools.wraps(func) 保留原函数名
6. 和 Java 注解最大区别: Python 装饰器真的改变行为!
""")

print("=" * 60)
print("✅ 主题 2-A 装饰器练习完成!")
print("看完输出后, 告诉我哪些预测错了, 我针对性讲解")
print("=" * 60)




