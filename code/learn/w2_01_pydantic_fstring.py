"""
W2 主题3 练习: f-string 高级 + pydantic 数据建模
================================================
教学目标: 能看懂并自己写 Ch7/Ch13 的数据模型
真实案例: 全部来自 Ch13 旅行助手后端 schemas.py

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_01_pydantic_fstring.py
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError


# ============================================================
# 第一部分: f-string 高级用法
# ============================================================
print("=" * 60)
print("第一部分: f-string 高级用法")
print("=" * 60)

city = "北京"
temperature = 30

# 1. 表达式嵌入
msg1 = f"{city}当前温度 {temperature * 2}℃"            ### 预测: ?
print(f"表达式: {msg1}")

# 2. 条件表达式
msg2 = f"温度{'偏高' if temperature > 28 else '正常'}"   ### 预测: ?
print(f"条件: {msg2}")

# 3. 格式化
price = 1234.5678
count = 1000000
progress = 0.758
print(f"精度: 价格 {price:.2f}")                         ### 预测: ?
print(f"千分位: {count:,}")                              ### 预测: ?
print(f"百分比: {progress:.1%}")                         ### 预测: ?

# 4. 多行 prompt 拼接 (Agent System Prompt 标准写法)
tools = ["天气查询", "景点推荐", "路线规划"]
system_prompt = f"""你是{city}旅行助手。

可用工具:
""" + "\n".join(f"- {t}" for t in tools)
print(f"\n多行 prompt:\n{system_prompt}")                ### 预测 system_prompt 的样子


# ============================================================
# 第二部分: pydantic 基础模型
# ============================================================
print("\n" + "=" * 60)
print("第二部分: pydantic BaseModel (Java POJO 升级版)")
print("=" * 60)

# Ch13 真实模型简化版
class Location(BaseModel):
    """地理位置"""
    longitude: float = Field(..., description="经度")
    latitude: float = Field(..., description="纬度")

class Attraction(BaseModel):
    """景点信息"""
    name: str = Field(..., description="景点名称")
    address: str = Field(..., description="地址")
    location: Location                                   # 嵌套模型!
    visit_duration: int = Field(..., ge=1, le=600, description="游览分钟数")
    ticket_price: int = Field(default=0, ge=0, description="门票价格")
    category: Optional[str] = Field(default="景点")
    photos: Optional[List[str]] = Field(default_factory=list)

# 创建实例 (类似 Java: new Attraction(...))
loc = Location(longitude=116.4, latitude=39.9)
attraction = Attraction(
    name="故宫",
    address="北京市东城区",
    location=loc,
    visit_duration=180
)
print(f"景点名: {attraction.name}")                       ### 预测: ?
print(f"经度: {attraction.location.longitude}")           ### 预测: ? (嵌套访问)
print(f"默认分类: {attraction.category}")                 ### 预测: ?
print(f"默认照片: {attraction.photos}")                   ### 预测: ?


# ============================================================
# 第三部分: 自动类型转换 (pydantic 比 Java 强的地方)
# ============================================================
print("\n" + "=" * 60)
print("第三部分: 自动类型转换")
print("=" * 60)

# 字符串数字自动转 int
a1 = Attraction(
    name="颐和园",
    address="海淀区",
    location={"longitude": "116.27", "latitude": "39.99"},  # 字符串自动转 float!
    visit_duration="240",                                    # 字符串转 int
    ticket_price="30"                                        # 字符串转 int
)
print(f"经度类型: {type(a1.location.longitude).__name__}")  ### 预测: ? (str 还是 float?)
print(f"时长类型: {type(a1.visit_duration).__name__}")      ### 预测: ?
print(f"经度值: {a1.location.longitude}")                   ### 预测: ?


# ============================================================
# 第四部分: 校验 (pydantic 最强功能)
# ============================================================
print("\n" + "=" * 60)
print("第四部分: 校验 (ge/le/自定义校验器)")
print("=" * 60)

# 1. 内置校验: ge (>=), le (<=), gt (>), lt (<), min_length, max_length
try:
    bad = Attraction(
        name="超时景点",
        address="某地",
        location=Location(longitude=116.0, latitude=39.0),
        visit_duration=999,                               ### 超过 le=600, 会怎样?
    )
except ValidationError as e:
    print(f"校验失败 (visit_duration=999):")
    print(f"  错误类型: {e.errors()[0]['type']}")          ### 预测: ?

# 2. 自定义校验器 (Ch13 schemas.py 真实用法)
class TripRequest(BaseModel):
    """Ch13 旅行请求"""
    city: str = Field(..., min_length=1)
    start_date: str
    end_date: str
    travel_days: int = Field(..., ge=1, le=30)

    @field_validator("city")
    @classmethod
    def city_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("城市名不能为空白")
        return v.strip()

try:
    req = TripRequest(city="  ", start_date="2025-01-01", end_date="2025-01-03", travel_days=3)
except ValidationError as e:
    print(f"\n自定义校验失败 (city为空白):")
    print(f"  错误: {e.errors()[0]['msg']}")               ### 预测: ?

# 正常请求
req_ok = TripRequest(city="北京", start_date="2025-01-01", end_date="2025-01-03", travel_days=3)
print(f"\n正常请求: {req_ok.city}, {req_ok.travel_days}天")


# ============================================================
# 第五部分: JSON 序列化 (Ch13 API 开发核心)
# ============================================================
print("\n" + "=" * 60)
print("第五部分: JSON 互转 (FastAPI 后端必备)")
print("=" * 60)

# 对象 → JSON (等价 Jackson writeValueAsString)
json_str = req_ok.model_dump_json()
print(f"对象→JSON: {json_str}")                           ### 预测: 长什么样?

# 对象 → dict
data_dict = req_ok.model_dump()
print(f"对象→dict: {data_dict}")                          ### 预测: ?
print(f"dict 类型: {type(data_dict).__name__}")

# JSON → 对象 (等价 Jackson readValue) - Ch13 接收前端请求就这么干
frontend_json = '{"city": "上海", "start_date": "2025-02-01", "end_date": "2025-02-05", "travel_days": 5}'
req_from_json = TripRequest.model_validate_json(frontend_json)
print(f"JSON→对象: {req_from_json.city}, {req_from_json.travel_days}天")   ### 预测: ?


# ============================================================
# 第六部分: 嵌套模型 (Agent 消息结构)
# ============================================================
print("\n" + "=" * 60)
print("第六部分: 嵌套模型 (OpenAI 消息结构)")
print("=" * 60)

class Message(BaseModel):
    """OpenAI 消息格式"""
    role: str
    content: str

class ChatRequest(BaseModel):
    """完整对话请求"""
    model: str
    messages: List[Message]                               # 嵌套列表!
    temperature: float = Field(default=0.7, ge=0, le=2)
    stream: bool = False

# 用 dict 构造 (pydantic 自动把 dict 转成 Message 对象)
request = ChatRequest(
    model="glm-4",
    messages=[
        {"role": "system", "content": "你是助手"},         # dict 自动转 Message
        {"role": "user", "content": "你好"}
    ]
)
print(f"第一条消息类型: {type(request.messages[0]).__name__}")  ### 预测: ? (dict 还是 Message?)
print(f"第一条消息: {request.messages[0].role}: {request.messages[0].content}")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("💡 今日核心 (Java 对照)")
print("=" * 60)
print("""
f-string:
  - {表达式} 可以放任何 Python 代码
  - :.2f 精度, :, 千分位, :.1% 百分比
  - 三引号 + f-string = 多行 prompt 模板

pydantic:
  - BaseModel 子类 = Java POJO + Lombok + Jackson + Bean Validation
  - Field(..., ge=1, le=30) = @NotNull + @Min(1) + @Max(30)
  - model_dump_json() = Jackson writeValueAsString()
  - model_validate_json() = Jackson readValue()
  - 自动类型转换 (字符串数字 → int)
  - 嵌套模型: List[Message] 自动解析

Ch13 的 schemas.py 就是这套技术的实战。
""")
