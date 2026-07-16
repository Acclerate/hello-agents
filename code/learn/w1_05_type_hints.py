"""
W1 主题2-B 练习: 类型注解 + typing 模块
========================================
教学目标: 能看懂 Ch7 自建框架所有函数签名
对应 Ch7 真实代码: my_llm.py / my_simple_agent.py / my_advanced_search.py

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w1_05_type_hints.py
"""
from typing import (
    Optional, List, Dict, Tuple, Any,
    Union, Callable, Iterator
)


# ============================================================
# 1. 基础类型注解 (和 Java 几乎一样)
# ============================================================
print("=" * 60)
print("练习1: 基础类型注解")
print("=" * 60)

# 变量类型注解 (可选, 但本书都用)
city: str = "北京"
temperature: int = 30
is_sunny: bool = True
price: float = 9.99

print(f"city: {city}, 类型注解告诉读者这是 str")
print(f"temperature: {temperature}, 这是 int")       ### 预测: ?

# 函数类型注解: 参数用 : 标注, 返回值用 -> 标注
# Java 等价: public String getWeather(String city) { ... }
def get_weather(city: str) -> str:
    return f"{city}: 晴朗"

# 返回 None (等价 Java 的 void)
def log_message(msg: str) -> None:
    print(f"[LOG] {msg}")

result = get_weather("上海")                          ### 预测: result = ?
log_message("调用成功")


# ============================================================
# 2. 集合类型 (Agent 代码里最多的结构!)
# ============================================================
print("\n" + "=" * 60)
print("练习2: 集合类型 (List / Dict / Tuple)")
print("=" * 60)

# List[str] = 字符串列表 (Java: List<String>)
cities: List[str] = ["北京", "上海", "深圳"]
print(f"cities 类型注解: List[str], 实际长度: {len(cities)}")

# Dict[str, str] = 字符串到字符串的映射 (Java: Map<String,String>)
# 这是 OpenAI API 的消息格式!
messages: List[Dict[str, str]] = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
]
# Java 等价: List<Map<String, String>>
print(f"消息数量: {len(messages)}")                    ### 预测: ?
print(f"第一条消息角色: {messages[0]['role']}")        ### 预测: ?

# Dict[str, Any] = 值可以是任意类型 (Java: Map<String, Object>)
# Ch7 配置对象的真实结构
config: Dict[str, Any] = {
    "model": "glm-4",                                 # str
    "temperature": 0.7,                               # float
    "max_tokens": 1000,                               # int
    "tools": ["search", "calc"],                      # list
    "stream": True                                    # bool
}
print(f"\nconfig 的值的类型各不相同:")
for key, value in config.items():
    print(f"  {key}: {type(value).__name__}")         ### 预测: model 是什么类型? tools 呢?

# Tuple[str, int] = 固定长度和类型的元组 (Java 没有直接对应)
# 场景: 函数返回多个值 (Python 特色, Java 要用类包装)
def parse_response(text: str) -> Tuple[str, str]:
    """返回 (思考过程, 行动)"""
    return ("分析天气", "调用天气API")

thought, action = parse_response("test")              ### 预测: thought=? action=?
print(f"\n解包返回: thought={thought}, action={action}")


# ============================================================
# 3. Optional[X] - Ch7 最高频的类型!
# ============================================================
print("\n" + "=" * 60)
print("练习3: Optional (Ch7 每个文件都用)")
print("=" * 60)

# Optional[str] = "str 或 None" (Ch7 的 __init__ 到处都是)
# 场景: 参数可有可无, 类似 Java 的 @Nullable
class LLMConfig:
    def __init__(
        self,
        model: Optional[str] = None,          # 可以不传
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7              # 有默认值但非 None
    ):
        # Python 惯用法: None + or 提供真实默认值
        self.model = model or "glm-4"         # 如果 model 是 None, 用 "glm-4"
        self.api_key = api_key or "default-key"
        self.base_url = base_url or "https://api.example.com/v1"
        self.temperature = temperature

# 三种调用方式
c1 = LLMConfig()                               ### model 会是什么?
c2 = LLMConfig(model="deepseek-v3")            ### model 会是什么?
c3 = LLMConfig(model=None, api_key="xxx")      ### model 会是什么? (注意显式传 None)

print(f"c1.model = {c1.model}")                ### 预测: ?
print(f"c2.model = {c2.model}")                ### 预测: ?
print(f"c3.model = {c3.model}")                ### 预测: ?
print(f"c3.api_key = {c3.api_key}")            ### 预测: ?


# ============================================================
# 4. Union 和 | (多类型选择)
# ============================================================
print("\n" + "=" * 60)
print("练习4: Union - 一个变量可以是多种类型")
print("=" * 60)

# Union[str, int] = 可以是 str 或 int
# Python 3.10+ 可以写成 str | int (更简洁)
def process_id(user_id: Union[str, int]) -> str:
    if isinstance(user_id, int):
        return f"数字ID: {user_id}"
    return f"字符串ID: {user_id}"

print(process_id(123))                          ### 预测: ?
print(process_id("abc"))                        ### 预测: ?

# Optional[X] 其实就是 Union[X, None] 的简写!
# Optional[str] ≡ Union[str, None] ≡ str | None


# ============================================================
# 5. Callable - 函数类型 (Ch7 注册回调时用)
# ============================================================
print("\n" + "=" * 60)
print("练习5: Callable (把函数当参数传递时的类型)")
print("=" * 60)

# Callable[[参数类型], 返回类型]
# Java 类比: Function<String, String> 或接口回调
def run_tool(tool_func: Callable[[str], str], input: str) -> str:
    """接收一个函数并执行 (Ch7 工具调度器就这么写)"""
    return tool_func(input)

def search(query: str) -> str:
    return f"搜索结果: {query}"

result = run_tool(search, "天气")                ### 预测: ?
print(f"结果: {result}")

# 更复杂的 Callable: 接收两个参数, 返回 bool
# Callable[[str, int], bool]  =  Java: BiFunction<String, Integer, Boolean>
validator: Callable[[str, int], bool] = lambda s, n: len(s) > n
print(f"验证: {validator('hello', 3)}")          ### 预测: ?


# ============================================================
# 6. Iterator - 迭代器 (Ch7 的 my_simple_agent.py 用)
# ============================================================
print("\n" + "=" * 60)
print("练习6: Iterator (Agent 流式响应用)")
print("=" * 60)

# Iterator[str] = 字符串迭代器 (Java: Iterator<String>)
# 场景: LLM 流式输出, 逐字返回
def stream_response(text: str) -> Iterator[str]:
    """模拟流式输出, 一个字一个字返回"""
    for char in text:
        yield char                    # yield = "暂停并返回一个值" (后面学)

print("流式输出: ", end="")
for chunk in stream_response("你好世界"):        ### 预测: 会怎么打印?
    print(chunk, end="", flush=True)
print()  # 换行


# ============================================================
# 7. 类型注解不强制! (重要认知)
# ============================================================
print("\n" + "=" * 60)
print("练习7: 类型注解不强制 (Python 和 Java 的根本区别)")
print("=" * 60)

def add(a: int, b: int) -> int:
    return a + b

# 类型注解说要 int, 但传 str 也能跑! (Python 不会阻止你)
result = add("hello", "world")         ### 预测: 会报错吗? 结果是什么?
print(f"add('hello', 'world') = {result}")
print("↑ 类型注解写的 int, 但 Python 不检查! 运行时照样拼接字符串")
print("  这就是为什么需要 mypy 做静态检查 (Ch14 会用到)")


# ============================================================
# 总结: Ch7 类型注解速查表
# ============================================================
print("\n" + "=" * 60)
print("💡 Ch7 类型注解速查表 (剪下来贴屏幕)")
print("=" * 60)
print("""
基础:     str | int | float | bool | None(=Java void)
集合:     List[str] | Dict[str, Any] | Tuple[str, int]
可选:     Optional[str] (= str 或 None, Ch7 最高频!)
多类型:   Union[str, int] (或 3.10+ 的 str | int)
函数:     Callable[[str], bool] (函数作为参数)
迭代:     Iterator[str] (流式/惰性计算)

★ Ch7 __init__ 标准签名 ★
  def __init__(
      self,
      model: Optional[str] = None,        # 可选参数
      api_key: Optional[str] = None,
      base_url: Optional[str] = None,
      **kwargs                             # 其余任意关键字参数
  ):

★ Python vs Java 根本区别 ★
  - 类型注解【不强制】, 运行时不检查
  - 需要 mypy/pyright 做【静态检查】
  - 类型注解主要是给【人和 IDE】看的
""")
