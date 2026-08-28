"""
装饰器三层嵌套拆解 (疑问2 专项)
================================
用「拆分法」理解带参数装饰器: 把三层一步步拆开, 分别调用, 看清楚每一层

运行:
cd D:\\privategit\\github\\Hello-Agents\\code\\learn
D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w1_03_decorator_3layers.py
"""
import functools

TOOL_REGISTRY = {}

# ============================================================
# 第一阶段: 完整的带参数装饰器 (三层)
# ============================================================
print("=" * 60)
print("阶段1: 完整的三层结构")
print("=" * 60)

def register_tool(name, description=""):           # 第1层: 接收参数
    print(f"  [第1层] register_tool 被调用, name={name}, desc={description}")#1
    def decorator(func):                            # 第2层: 接收函数
        print(f"    [第2层] decorator 被调用, func={func.__name__}") #3
        TOOL_REGISTRY[name] = {"func": func, "desc": description}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):               # 第3层: 接收调用参数 #4
            print(f"      [第3层] wrapper 被调用, args={args}")
            return func(*args, **kwargs)
        print(f"    [第2层] 返回 wrapper")
        return wrapper
    print(f"  [第1层] 返回 decorator (一个还没执行的函数)") #2
    return decorator


# ============================================================
# 第二阶段: 用 @ 语法 (你会看到定义时就执行了第1层和第2层!)
# ============================================================
print("\n" + "=" * 60)
print("阶段2: 用 @ 语法 (注意定义阶段就打印了什么!)")
print("=" * 60)

@register_tool("weather", "查询天气")
def get_weather(city):
    """天气工具"""
    return f"{city}: 晴"

# 看上面的输出! 你会发现:
# - 第1层和第2层在【定义函数时】就执行了 (import 时)
# - 第3层 wrapper 在【调用时】才执行
# 这就是为什么装饰器"注册"功能能自动生效!

print(f"\n此时 TOOL_REGISTRY = {list(TOOL_REGISTRY.keys())}")

#   [第1层] register_tool 被调用, name=weather, desc=查询天气
#   [第1层] 返回 decorator (一个还没执行的函数)
#     [第2层] decorator 被调用, func=get_weather
#     [第2层] 返回 wrapper

# ============================================================
# 第三阶段: 手动拆解! 等价于 @ 语法, 但一步步来
# ============================================================
print("\n" + "=" * 60)
print("阶段3: 手动拆解 (和 @ 语法完全等价, 但看清每一步)")
print("=" * 60)

TOOL_REGISTRY.clear()

# 第1步: 定义原始函数 (不被装饰)
def get_temperature(city):
    """温度工具"""
    return f"{city}: 30度"

print(f"第1步: 定义原始函数 {get_temperature.__name__}")

# 第2步: 手动调用 register_tool (它会返回 decorator)
my_decorator = register_tool("temperature", "查询温度")
print(f"第2步: register_tool 返回了: {my_decorator.__name__}")
# 注意: my_decorator 现在是 decorator 函数, 还没应用到任何东西!

# 第3步: 手动调用 decorator(原函数)
get_temperature = my_decorator(get_temperature)
print(f"第3步: decorator 应用后, get_temperature 现在指向: {get_temperature.__name__}")
# 注意: 此时 get_temperature 已经是 wrapper 了 (但 functools.wraps 保住了名字)

# 第4步: 调用
print(f"\n第4步: 调用 get_temperature('北京')")
result = get_temperature("北京")
print(f"结果: {result}")

print(f"\nTOOL_REGISTRY = {list(TOOL_REGISTRY.keys())}")


# ============================================================
# 第四阶段: Java 类比总结
# ============================================================
print("\n" + "=" * 60)
print("Java 程序员记忆图")
print("=" * 60)
print("""
@register_tool("weather", "查询天气")   # 带参数
def get_weather(city): ...

等价 Java 伪代码:

  // 第1层 = 工厂方法 (接收参数, 返回一个装饰器)
  Function<F, F> registerTool(String name, String desc) {
      // 第2层 = 返回的装饰器 (接收原函数, 返回包装函数)
      return (func) -> {
          TOOL_REGISTRY.put(name, func);          // 副作用: 注册
          // 第3层 = 包装函数 (转发调用)
          return (args) -> func.apply(args);
      };
  }

  // @register_tool("weather", "查询天气") 等价于:
  get_weather = registerTool("weather", "查询天气").apply(get_weather);

口诀:
  第1层管【参数】 (name, description)
  第2层管【函数】 (被装饰的 func)
  第3层管【调用】 (实际传给函数的 args)
""")
