"""
装饰器疑问 3 项 - 综合验证练习
===============================
覆盖: 1. *args/**kwargs 参数转发 + functools.wraps
      2. 带参数装饰器三层嵌套
      3. @property / @x.setter 读写机制

先预测 ### 处的输出, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w1_04_property_kwargs.py
"""
import functools

# ============================================================
# 验证 1: *args/**kwargs 的打包与解包
# ============================================================
print("=" * 60)
print("验证1: *args/**kwargs")
print("=" * 60)

def show_params(*args, **kwargs):
    print(f"  args (tuple) = {args}")
    print(f"  kwargs (dict) = {kwargs}")

print("调用 show_params(1, 2, 3):")
show_params(1, 2, 3)                         ### 预测: args=? kwargs=?

print("\n调用 show_params(name='x', age=20):")
show_params(name='x', age=20)                ### 预测: args=? kwargs=?

print("\n调用 show_params(1, 2, name='x'):")
show_params(1, 2, name='x')                  ### 预测: args=? kwargs=?

# 解包: * 和 ** 的反向操作
print("\n解包传递:")
data_tuple = (10, 20)
data_dict = {"name": "test"}
print("调用 show_params(*data_tuple, **data_dict):")
show_params(*data_tuple, **data_dict)        ### 预测: 和上面哪个一样?


# ============================================================
# 验证 2: 三层装饰器的定义时机
# ============================================================
print("\n" + "=" * 60)
print("验证2: 三层装饰器 (注意定义阶段 vs 调用阶段)")
print("=" * 60)

REGISTRY = {}

def tool(name, version="1.0"):
    def decorator(func):
        REGISTRY[name] = {"func": func, "version": version}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 下面这两行在"定义阶段"就会执行第1层和第2层
@tool("search", "2.0")
def web_search(query, max_results=5):
    """搜索工具"""
    return f"搜索 '{query}', 返回 {max_results} 条"

# 定义阶段执行了什么?
print(f"定义后, REGISTRY = {REGISTRY}")       ### 预测: REGISTRY 里有啥?

# 调用阶段
result = web_search("天气", max_results=3)    ### 预测: result = ?
print(f"调用结果: {result}")

# functools.wraps 的效果
print(f"函数名: {web_search.__name__}")       ### 预测: ? (wrapper 还是 web_search?)
print(f"文档: {web_search.__doc__}")          ### 预测: ?


# ============================================================
# 验证 3: @property 读写拦截
# ============================================================
print("\n" + "=" * 60)
print("验证3: @property 读写拦截")
print("=" * 60)

class AgentConfig:
    def __init__(self, model="gpt-4", max_tokens=1000):
        self._model = model
        self._history = []
        self._max_tokens = max_tokens

    @property
    def model(self):
        return self._model.upper()           # 动态处理: 返回大写

    @model.setter
    def model(self, value):
        if not value:
            raise ValueError("model 不能为空")
        self._model = value

    @property
    def history_count(self):                 # 计算属性, 不存储
        return len(self._history)

    def add_message(self, msg):
        self._history.append(msg)

config = AgentConfig(model="glm-4")

print(f"config.model = {config.model}")      ### 预测: ? (注意 .upper())
print(f"config.history_count = {config.history_count}")  ### 预测: ?

config.model = "deepseek"                    ### 会调用 setter
print(f"改后 config.model = {config.model}") ### 预测: ?

config.add_message("你好")
config.add_message("在吗")
print(f"config.history_count = {config.history_count}")  ### 预测: ?

# 触发校验
print("\n尝试设置空 model:")
try:
    config.model = ""                        ### 会抛异常吗?
except ValueError as e:
    print(f"  捕获异常: {e}")


# ============================================================
# 总结对照表
# ============================================================
print("\n" + "=" * 60)
print("💡 三大疑问 - 一句话总结")
print("=" * 60)
print("""
1. *args/**kwargs
   = 通用参数容器, 让 wrapper 能适配任何签名的原函数
   = Java 的 Object... args 的增强版 (能区分位置参数和关键字参数)

2. 带参数装饰器三层嵌套
   第1层管参数, 第2层管函数, 第3层管调用
   = @tool("name") 先执行 tool("name") 返回真正的装饰器
   = Java 的工厂方法返回包装器

3. @property / @x.setter
   = 把方法伪装成字段, 实现受控读写
   = Java 的 getter/setter 的优雅版
   = 好处: 动态计算属性、写入校验、只读控制
""")
