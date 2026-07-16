"""
W1 主题1 练习：Python 核心语法对照 Java
=========================================
练习方法：
  1. 先读代码，在每处 ### 处预测输出（写在注释里）
  2. 然后运行本文件：python w1_01_basics.py
  3. 对照实际输出，修正理解

运行方式（用 hello-agents 环境）：
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w1_01_basics.py
"""

# ============ 1. 变量与动态类型 ============
print("=" * 50)
print("练习 1: 变量与动态类型")
print("=" * 50)

x = 10            # 现在是 int
print(f"x = {x}, 类型 = {type(x).__name__}")   ### 预测:int ?

x = "北京"        # 同一变量改成 str (Java 里会编译错误!)
print(f"x = {x}, 类型 = {type(x).__name__}")   ### 预测: str?

API_KEY = "abc123"   # 约定: 常量用大写, 但 Python 不强制
print(f"API_KEY = {API_KEY}")                   ### 预测: abc123?


# ============ 2. 控制流: if/elif/else ============
print("\n" + "=" * 50)
print("练习 2: 控制流 (注意缩进!)")
print("=" * 50)

temperature = 30

# 注意: 冒号 + 缩进, 不是花括号
if temperature > 35:
    print("酷热")            ### temperature=30 时会执行吗?
elif temperature > 15:
    print("舒适")
elif temperature > 25:
    print("炎热")            ### 预测: ?
else:
    print("凉爽")


# ============ 3. for 循环 (Python 的 for 是 for-each) ============
print("\n" + "=" * 50)
print("练习 3: for 循环")
print("=" * 50)

# range(5) = 0,1,2,3,4 (和 Java for(int i=0;i<5;i++) 一样)
print("range(5):")
for i in range(5):
    print(f"  循环 {i}")     ### 预测: 会打印几行? i 的范围?

# 遍历列表 (对应 Java 的 for-each)
cities = ["北京", "上海", "深圳"]
print("\n遍历城市列表:")
for city in cities:          ### 预测: ?
    print(f"  {city}")

# 遍历字典 (Agent 代码里大量出现)
# 字典 = Java 的 Map<String, Object>
config = {"model": "glm-4", "temperature": 0.7, "max_tokens": 1000}
print("\n遍历配置字典:")
for key, value in config.items():   ### 预测: 会打印几行?
    print(f"  {key} = {value}")


# ============ 4. 字符串处理 (f-string, Agent prompt 核心) ============
print("\n" + "=" * 50)
print("练习 4: f-string (Agent 拼接 prompt 的核心技能)")
print("=" * 50)

city = "北京"
weather = "晴朗"

# f-string: 字符串前加 f, 用 {} 嵌入变量
# 对应 Java: String.format("%s今天%s", city, weather) 但更简洁
prompt = f"查询{city}的天气，当前{weather}"
print(prompt)                ### 预测: ?

# 多行字符串 (用三引号), FirstAgentTest.py 的 system prompt 就是这么写的
system_prompt = f"""
你是一个助手。
城市: {city}
天气: {weather}*
任务: 推荐景点
"""
print("\n多行字符串:")        ### 预测 system_prompt 长什么样?
print(system_prompt)


# ============ 5. 函数定义 ============
print("=" * 50)
print("练习 5: 函数定义 (对比 Java 方法)")
print("=" * 50)

# Python 用 def 定义函数, -> str 是返回类型注解 (可选)
def get_weather(city: str) -> str:
    """查询天气 (这是文档字符串 docstring)"""
    return f"{city}: 晴朗 30℃"

# 对应 Java:
# public String getWeather(String city) {
#     return city + ": 晴朗 30℃";
# }

print(get_weather("北京"))    ### 预测: ?

# Python 特有: 默认参数, 关键字调用 (Agent 工具调用常用)
def search(query: str, max_results: int = 5, lang: str = "zh"):
    return f"搜索'{query}', 最多{max_results}条, 语言{lang}"

print(search("景点"))                          ### 预测: ? (用默认值)
print(search("景点", max_results=10))          ### 预测: ? (指定某个参数)
print(search("景点", lang="en", max_results=3) )  ### 预测: ? (乱序指定)


# ============ 6. 异常处理 ============
print("\n" + "=" * 50)
print("练习 6: 异常处理 (FirstAgentTest.py 里到处都是)")
print("=" * 50)

# Python: try/except (Java: try/catch)
def call_api(url: str):
    try:
        # 模拟 API 调用
        if "error" in url:
            raise ValueError("API 返回错误")  # 对应 Java: throw new
        print(f"调用 {url} 成功")
    except ValueError as e:
        # 对应 Java: catch (ValueError e)
        print(f"捕获异常: {e}")
    except Exception as e:
        # 对应 Java: catch (Exception e) 兜底
        print(f"未知异常: {e}")
    finally:
        print("清理资源 (finally, 和 Java 一样)")

call_api("https://api.example.com/weather")   ### 预测: 打印哪几行?
call_api("https://api.example.com/error")     ### 预测: 打印哪几行?


print("\n" + "=" * 50)
print("✅ 练习 1 完成! 检查你的预测和实际输出是否一致")
print("不一致的地方就是你需要重点理解的点")
print("=" * 50)
