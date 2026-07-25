"""
W2 pydantic 深度练习 (主题3 强化)
==================================
覆盖: 字段定义 / 必填默认值 / Field 约束 / 类型转换 / 嵌套模型 / 校验器 / JSON
对照 Ch13 schemas.py 的真实写法

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_02_pydantic_deep.py
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError


# ============================================================
# 第一层: 字段定义的 4 种姿势
# ============================================================
print("=" * 60)
print("第一层: 字段定义的 4 种姿势")
print("=" * 60)

class Product(BaseModel):
    # 姿势1: 直接写类型 = 必填 (不提供会报错)
    name: str
    # 姿势2: 类型 + 字面量默认值
    stock: int = 0
    # 姿势3: Optional + None (明确表示"可以没有")
    description: Optional[str] = None
    # 姿势4: Field() 增强约束 (推荐, Ch13 用法)
    price: float = Field(..., gt=0, description="价格必须>0")
    tags: List[str] = Field(default_factory=list, description="标签")

# 创建实例
p = Product(name="手机", price=4999.99)
print(f"p.name = {p.name}")                          ### 预测: ?
print(f"p.stock = {p.stock}")                        ### 预测: ? (没传用什么?)
print(f"p.description = {p.description}")            ### 预测: ?
print(f"p.tags = {p.tags}")                          ### 预测: ?
print(f"p.price = {p.price}")                        ### 预测: ?

# 缺必填字段会怎样?
try:
    Product(price=100)                               ### name 没传, 会怎样?
except ValidationError as e:
    print(f"\n缺 name 的错误: {e.errors()[0]['msg']}")   ### 预测: ?


# ============================================================
# 第二层: Field() 约束全家桶
# ============================================================
print("\n" + "=" * 60)
print("第二层: Field() 约束全家桶")
print("=" * 60)

class StrictModel(BaseModel):
    # 数值约束
    age: int = Field(ge=0, le=150, description="年龄0-150")
    # 字符串长度
    username: str = Field(min_length=3, max_length=20)
    # 正则匹配 (类似 Java @Pattern)
    phone: str = Field(pattern=r"^1[3-9]\d{9}$", description="手机号")
    # 集合约束
    tags: List[str] = Field(default_factory=list, max_length=5)  # 最多5个

# 合法数据
ok = StrictModel(age=25, username="zhangsan", phone="13800138000")
print(f"合法数据: {ok.username}, {ok.phone}")        ### 预测: ?

# 各种校验失败 (逐个看错误类型)
test_cases = [
    ("年龄超限", {"age": 200, "username": "abc", "phone": "13800138000"}),
    ("用户名太短", {"age": 20, "username": "ab", "phone": "13800138000"}),
    ("手机号格式错", {"age": 20, "username": "abc", "phone": "12345"}),
]
for name, data in test_cases:
    try:
        StrictModel(**data)
        print(f"{name}: 通过(没想到吧)")
    except ValidationError as e:
        err = e.errors()[0]
        print(f"{name}: 失败 [{err['type']}] {err['msg']}")   ### 预测各种错误类型?


# ============================================================
# 第三层: 自动类型转换 (pydantic 比Java强的地方)
# ============================================================
print("\n" + "=" * 60)
print("第三层: 自动类型转换 (智能转换, 不是傻傻报错)")
print("=" * 60)

class ConvertDemo(BaseModel):
    count: int
    price: float
    active: bool
    name: str

# 传"字符串数字"会自动转换 (Ch13 经常这样接收前端数据)
demo = ConvertDemo(count="100", price="9.99", active="true", name=123)
print(f"count: 值={demo.count}, 类型={type(demo.count).__name__}")   ### 预测类型?
print(f"price: 值={demo.price}, 类型={type(demo.price).__name__}")   ### 预测类型?
print(f"active: 值={demo.active}, 类型={type(demo.active).__name__}") ### 预测类型?
print(f"name: 值={demo.name}, 类型={type(demo.name).__name__}")      ### 预测类型? (int→str?)

# 注意: 转换不了才会报错
try:
    ConvertDemo(count="abc", price=10, active=True, name="x")      ### count="abc"
except ValidationError as e:
    print(f"\ncount='abc' 错误: {e.errors()[0]['msg']}")            ### 预测: ?


# ============================================================
# 第四层: 嵌套模型 (Agent 消息结构)
# ============================================================
print("\n" + "=" * 60)
print("第四层: 嵌套模型 (OpenAI 消息 / Ch13 Location+Attraction)")
print("=" * 60)

class Location(BaseModel):
    """Ch13 真实模型"""
    longitude: float
    latitude: float

class Attraction(BaseModel):
    """Ch13 真实模型 (嵌套 Location)"""
    name: str
    location: Location                              # 嵌套模型!
    visit_duration: int = Field(gt=0)

# 方式1: 用模型对象构造
loc = Location(longitude=116.4, latitude=39.9)
a1 = Attraction(name="故宫", location=loc, visit_duration=180)
print(f"方式1 经度: {a1.location.longitude}")       ### 预测: ?

# 方式2: 用 dict 构造 (pydantic 自动转成 Location 对象!)
a2 = Attraction(
    name="颐和园",
    location={"longitude": 116.27, "latitude": 39.99},   # dict 自动转 Location!
    visit_duration=240
)
print(f"方式2 location 类型: {type(a2.location).__name__}")   ### 预测: ? (dict 还是 Location?)
print(f"方式2 经度: {a2.location.longitude}")                ### 预测: ?

# 嵌套校验: 内层 location 字段错也会报错
try:
    Attraction(name="x", location={"longitude": "abc"}, visit_duration=10)  ### 会怎样?
except ValidationError as e:
    print(f"嵌套校验失败: {e.errors()[0]['loc']}")           ### 预测: loc 字段路径?


# ============================================================
# 第五层: 自定义校验器 (Ch13 schemas.py 真实用法)
# ============================================================
print("\n" + "=" * 60)
print("第五层: 自定义校验器 (Ch13 field_validator)")
print("=" * 60)

class TripRequest(BaseModel):
    """Ch13 真实模型简化版"""
    city: str = Field(..., min_length=1)
    start_date: str
    end_date: str
    travel_days: int = Field(..., ge=1, le=30)

    # @field_validator: 对单个字段加自定义校验
    # @classmethod: 因为校验方法是类方法 (Ch7 学过!)
    # 返回值: 处理后的值 (可以修改!)
    @field_validator("city")
    @classmethod
    def city_must_not_be_blank(cls, v: str) -> str:
        """去除首尾空格, 且不能全是空白"""
        v = v.strip()                               # 顺便做数据处理
        if not v:
            raise ValueError("城市名不能为空白")
        return v

    @field_validator("travel_days")
    @classmethod
    def days_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("天数必须大于0")
        return v

# 校验: 空白城市
try:
    TripRequest(city="   ", start_date="2025-01-01", end_date="2025-01-03", travel_days=3)
except ValidationError as e:
    print(f"空白城市错误: {e.errors()[0]['msg']}")   ### 预测: ?

# 校验: 正常 + 数据处理 (注意 city 被自动 strip!)
req = TripRequest(city="  北京  ", start_date="2025-01-01", end_date="2025-01-03", travel_days=3)
print(f"strip 后的 city: '{req.city}'")              ### 预测: ? (注意空格!)


# ============================================================
# 第六层: JSON 互转 (FastAPI 后端核心操作)
# ============================================================
print("\n" + "=" * 60)
print("第六层: JSON 互转 (API 开发每天用)")
print("=" * 60)

req = TripRequest(city="上海", start_date="2025-02-01", end_date="2025-02-05", travel_days=5)

# 1. model_dump() → dict (Ch13 后端把数据传给 LLM 时用)
d = req.model_dump()
print(f"model_dump() 类型: {type(d).__name__}")      ### 预测: ?
print(f"内容: {d}")                                   ### 预测: ?

# 2. model_dump_json() → JSON 字符串 (返回给前端)
j = req.model_dump_json()
print(f"model_dump_json(): {j}")                      ### 预测: 长什么样?

# 3. model_validate(dict) → 从 dict 创建 (Ch13 接收前端数据)
req2 = TripRequest.model_validate({
    "city": "深圳",
    "start_date": "2025-03-01",
    "end_date": "2025-03-03",
    "travel_days": 3
})
print(f"从dict创建: {req2.city}")                     ### 预测: ?

# 4. model_validate_json(str) → 从 JSON 创建 (FastAPI 自动做这步)
req3 = TripRequest.model_validate_json(
    '{"city":"广州","start_date":"2025-04-01","end_date":"2025-04-03","travel_days":3}'
)
print(f"从JSON创建: {req3.city}")                     ### 预测: ?


# ============================================================
# 第七层: 实战 - 完整 Agent 配置模型
# ============================================================
print("\n" + "=" * 60)
print("第七层: 实战 - 完整 Agent 配置 (综合运用)")
print("=" * 60)

class ToolConfig(BaseModel):
    """工具配置 (Ch7 工具系统的核心数据结构)"""
    name: str = Field(..., min_length=1, description="工具名")
    description: str = Field(default="", description="工具描述")
    enabled: bool = Field(default=True)

class AgentConfig(BaseModel):
    """Agent 完整配置 (综合所有特性)"""
    # 基础字段
    name: str = Field(..., description="Agent名称")
    model: str = Field(default="glm-4", description="LLM模型")
    temperature: float = Field(default=0.7, ge=0, le=2)

    # 嵌套模型
    system_prompt: str = Field(..., min_length=10, description="系统提示词")
    tools: List[ToolConfig] = Field(default_factory=list)

    # Optional
    max_iterations: Optional[int] = Field(default=10, gt=0)

    # 自定义校验
    @field_validator("name")
    @classmethod
    def name_normalized(cls, v: str) -> str:
        return v.strip().lower()                     # 统一小写

    @field_validator("system_prompt")
    @classmethod
    def prompt_must_have_role(cls, v: str) -> str:
        if "你" not in v and "you" not in v.lower():
            raise ValueError("system_prompt 应该描述 Agent 角色")
        return v

# 构造完整的 Agent 配置 (用 dict, 模拟从 JSON 配置文件读取)
config_data = {
    "name": "  TravelBot  ",                         # 故意带空格和大写
    "model": "glm-4",
    "system_prompt": "你是一个旅行助手,帮助用户规划行程。",
    "tools": [
        {"name": "weather", "description": "查天气"},
        {"name": "search", "description": "搜索景点", "enabled": False}
    ],
    "max_iterations": 20
}

agent = AgentConfig.model_validate(config_data)
print(f"规范化名称: '{agent.name}'")                  ### 预测: ? (小写+去空格)
print(f"工具数量: {len(agent.tools)}")                ### 预测: ?
print(f"第一个工具: {agent.tools[0].name}")           ### 预测: ?
print(f"第二个工具启用: {agent.tools[1].enabled}")     ### 预测: ?
print(f"模型: {agent.model}, 温度: {agent.temperature}")   ### 预测: ?

# 序列化为 JSON (保存配置)
print(f"\n完整配置 JSON:")
print(agent.model_dump_json(indent=2))               ### 预测: 长什么样?


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("💡 pydantic BaseModel 核心速查")
print("=" * 60)
print("""
字段定义:
  name: str                              # 必填
  age: int = 18                          # 默认值
  email: Optional[str] = None            # 可选
  score: float = Field(ge=0, le=100)     # 带约束

Field 参数:
  ...           必填标记 (第一个位置参数)
  ge/le/gt/lt   >= / <= / > / <
  min_length/max_length  字符串长度
  pattern        正则
  default_factory=list   可变默认值 (避免共享陷阱)

校验:
  @field_validator("字段名") + @classmethod
  抛 ValueError 或返回处理后的值

序列化 (FastAPI 后端核心):
  model_dump()              → dict
  model_dump_json()         → JSON 字符串
  model_validate(dict)      ← dict 创建对象
  model_validate_json(str)  ← JSON 创建对象

嵌套模型:
  嵌套字段可以用 dict 构造, pydantic 自动转换
  内层校验失败会精确报告字段路径 (loc)

Java 对照:
  BaseModel ≡ POJO + Lombok + Jackson + Bean Validation
""")
