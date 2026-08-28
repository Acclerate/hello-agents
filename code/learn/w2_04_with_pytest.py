"""
W2 主题4-B 练习: with 上下文管理器 + pytest 测试
=================================================
教学目标: 能看懂 Ch9 的沙箱工具 + 能写 Ch7 风格的测试
真实出处:
  - Ch9 的 TerminalTool (沙箱 shell, 用 with 管理资源)
  - Ch7 的 test_*.py (pytest 测试模式)

★ Java 程序员的认知迁移 ★
  Python with ≈ Java try-with-resources (Java 7+)
  pytest ≈ JUnit 5 (但更简洁, 不需要注解)

先预测 ### 处, 再运行对照。

运行:
  cd D:\\privategit\\github\\Hello-Agents\\code\\learn
  D:\\ProgramData\\my_custom_envs\\hello-agents\\python.exe w2_04_with_pytest.py
"""
import pytest
from typing import Optional


# ============================================================
# 第一部分: with 语句基础 (资源管理)
# ============================================================
print("=" * 60)
print("第一部分: with 语句 (资源管理)")
print("=" * 60)

# ★ Java 程序员的熟悉感 ★
# Python:                           Java (7+):
# with open(f) as fh:               try (FileReader fr = new FileReader(f)) {
#     fh.read()                         fr.read();
#                                   }
# with 会自动关闭资源, 即使抛异常

# 文件操作 (最常见的 with 用法)
print("--- 文件操作 ---")
with open("test_with.txt", "w", encoding="utf-8") as f:
    f.write("hello")                            # 不需要 f.close()! with 自动关
    print(f"  写入时文件是否关闭: {f.closed}")    ### 预测: ? (True/False)
print(f"  with 结束后文件是否关闭: {f.closed}")    ### 预测: ? (应该 True!)

# 读文件
with open("test_with.txt", encoding="utf-8") as f:
    content = f.read()
print(f"  读到的内容: {content}")

# 即使 with 内部抛异常, 资源也会关闭
try:
    with open("test_with.txt", encoding="utf-8") as f:
        raise ValueError("故意出错")             ### 会关闭文件吗?
        f.read()                                 # 不会执行到
except ValueError:
    print(f"  异常后文件是否关闭: {f.closed}")    ### 预测: ? (True!)


# ============================================================
# 第二部分: 自定义上下文管理器 (Ch9 沙箱工具的核心)
# ============================================================
print("\n" + "=" * 60)
print("第二部分: 自定义上下文管理器")
print("=" * 60)

# 方式1: 实现 __enter__ / __exit__ 协议 (类的方式)
class Timer:
    """计时器 (with 进入时启动, 退出时报时)"""
    def __enter__(self):
        import time
        self.start = time.time()
        print("  [Timer] 开始计时")
        return self                              # as timer 拿到的就是 self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.time() - self.start
        print(f"  [Timer] 结束, 耗时 {self.elapsed:.4f}s")
        # exc_type: 异常类型 (None 表示没异常)
        # 返回 False/None = 异常继续传播; 返回 True = 吞掉异常
        return False                             # 让异常正常传播

# 使用
print("--- 类方式 ---")
with Timer() as timer:
    sum(range(1000000))                          ### 预测: with 结束会打印啥?


# 方式2: @contextmanager 装饰器 (更简洁, 推荐)
from contextlib import contextmanager

@contextmanager
def mock_agent_context(agent_name: str):
    """模拟 Agent 会话 (Ch9 沙箱风格)"""
    print(f"  [{agent_name}] 会话开始")
    state = {"messages": [], "active": True}     # 进入时的状态
    try:
        yield state                              # yield 之前 = __enter__
        # yield 之后 = __exit__
    finally:
        state["active"] = False                  # 清理
        print(f"  [{agent_name}] 会话结束, 消息数: {len(state['messages'])}")

print("\n--- contextmanager 方式 ---")
with mock_agent_context("TravelBot") as ctx:
    ctx["messages"].append("你好")               ### 预测: yield 出来的 state 能改吗?
    ctx["messages"].append("推荐景点")
    print(f"  会话内消息: {ctx['messages']}")    ### 预测: ?


# ============================================================
# 第三部分: 实战 - Ch9 沙箱 Shell 工具模拟
# ============================================================
print("\n" + "=" * 60)
print("第三部分: 实战 - 沙箱 Shell (Ch9 TerminalTool 简化版)")
print("=" * 60)

@contextmanager
def sandbox_shell(allowed_commands: list):
    """模拟 Ch9 的 TerminalTool (命令白名单 + 超时)"""
    print(f"  [Sandbox] 启动, 允许: {allowed_commands}")
    active = True
    def execute(cmd: str) -> str:
        if not active:
            return "错误: 沙箱已关闭"
        cmd_name = cmd.split()[0]
        if cmd_name not in allowed_commands:
            return f"错误: '{cmd_name}' 不在白名单"
        return f"执行: {cmd} → 成功"

    try:
        yield execute                            # 暴露 execute 函数给用户
    finally:
        active = False                           # 退出时禁用
        print(f"  [Sandbox] 关闭")

# 使用 (模拟 Ch9 的 Agent 调用 shell)
print("--- 沙箱执行 ---")
with sandbox_shell(["ls", "cat", "echo"]) as run:
    print(f"  {run('ls -la')}")                  ### 预测: ?
    print(f"  {run('echo hello')}")              ### 预测: ?
    print(f"  {run('rm -rf /')}")                ### 预测: ? (危险命令被拦截!)

# with 结束后再调用
print(f"  with结束后: {run('ls')}")              ### 预测: ? (沙箱已关)


# ============================================================
# 第四部分: pytest 基础 (Ch7 测试风格)
# ============================================================
print("\n" + "=" * 60)
print("第四部分: pytest 基础 (对比 JUnit)")
print("=" * 60)

# ★ pytest vs JUnit ★
# JUnit:                          pytest:
# @Test                           def test_xxx():  (命名约定: test_ 开头)
# void testXxx() {                (不需要注解)
#     assertEquals(4, add(2,2));      assert add(2, 2) == 4
# }

# 被测函数
def add(a, b):
    return a + b

def get_weather(city):
    return f"{city}: 晴"

# pytest 测试函数 (命名必须 test_ 开头)
def test_add():
    assert add(2, 3) == 5                        # assert = JUnit 的 assertEquals
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_add_negative():
    assert add(-1, -1) == -2

def test_get_weather():
    result = get_weather("北京")
    assert "北京" in result                      # assert in = 包含检查
    assert "晴" in result

# 直接运行本文件时, 调用 pytest 跑测试
print("--- 运行 pytest ---")
# pytest.main 会执行本文件所有 test_ 开头的函数
exit_code = pytest.main([__file__, "-v", "--tb=short"])
print(f"\npytest 退出码: {exit_code} (0 = 全部通过)")


# ============================================================
# 第五部分: pytest 进阶 (fixture + 参数化)
# ============================================================
# 这部分只在被 pytest 收集时才跑 (下面的代码用 if 守卫)
print("\n" + "=" * 60)
print("第五部分: pytest 进阶 (fixture + 参数化)")
print("=" * 60)

# fixture = 测试前的准备工作 (JUnit @BeforeEach)
# 参数化 = 数据驱动测试 (JUnit @ParameterizedTest)

# --- fixture 示例 ---
@pytest.fixture
def sample_agent():
    """每个测试用例都会拿到这个 fixture 的返回值"""
    # setup (准备工作)
    agent = {"name": "TestBot", "history": [], "model": "glm-4"}
    yield agent                                  # 提供给测试用例
    # teardown (清理工作, 可选)
    agent["history"].clear()

def test_agent_initialization(sample_agent):     # 参数名 = fixture 名
    assert sample_agent["name"] == "TestBot"
    assert sample_agent["history"] == []
    assert sample_agent["model"] == "glm-4"

def test_agent_add_message(sample_agent):
    sample_agent["history"].append("你好")
    assert len(sample_agent["history"]) == 1
    # 注意: 每个测试的 fixture 是独立的 (不会互相影响)


# --- 参数化测试 ---
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),                                   # 测试数据1
    (10, 20, 30),                                # 测试数据2
    (-1, 1, 0),                                  # 测试数据3
    (100, 200, 300),                             # 测试数据4
])
def test_add_parametrized(a, b, expected):
    """参数化: 一组数据跑多个测试用例"""
    assert add(a, b) == expected


# --- 异常测试 (测试应该抛异常的情况) ---
def test_divide_by_zero():
    """测试除零应该抛 ZeroDivisionError"""
    with pytest.raises(ZeroDivisionError):       ### 预测: 这个测试通过吗?
        1 / 0

def test_value_error():
    with pytest.raises(ValueError) as exc_info:
        int("不是数字")
    assert "invalid literal" in str(exc_info.value)


# ============================================================
# 第六部分: 实战 - 测试 Agent 组件 (Ch7 风格)
# ============================================================
print("\n" + "=" * 60)
print("第六部分: 实战 - 测试 Agent 工具 (Ch7 风格)")
print("=" * 60)

# 模拟 Ch7 的工具类
class CalculatorTool:
    """计算器工具 (Ch7 my_calculator_tool.py 简化版)"""
    name = "calculator"
    description = "数学计算"

    def execute(self, expression: str) -> str:
        try:
            # 危险! 实际项目不要用 eval (这里仅演示)
            result = eval(expression)            ### 别在真实代码用 eval!
            return str(result)
        except Exception as e:
            return f"错误: {e}"

# 测试 fixture
@pytest.fixture
def calc():
    return CalculatorTool()

# 测试用例
def test_calc_add(calc):
    assert calc.execute("2 + 3") == "5"

def test_calc_subtract(calc):
    assert calc.execute("10 - 4") == "6"

def test_calc_multiply(calc):
    assert calc.execute("6 * 7") == "42"

def test_calc_divide(calc):
    assert calc.execute("15 / 3") == "5.0"

def test_calc_error(calc):
    result = calc.execute("1 / 0")
    assert "错误" in result                       ### 预测: ? (除零返回啥?)

@pytest.mark.parametrize("expr, expected", [
    ("1 + 1", "2"),
    ("2 * 3", "6"),
    ("10 - 5", "5"),
    ("8 / 2", "4.0"),
])
def test_calc_parametrized(calc, expr, expected):
    assert calc.execute(expr) == expected


# ============================================================
# 第七部分: pytest 运行方式
# ============================================================
print("\n" + "=" * 60)
print("第七部分: pytest 运行方式")
print("=" * 60)
print("""
命令行运行 (在项目根目录):
  pytest                          # 运行所有 test_*.py
  pytest -v                       # 详细输出 (显示每个测试名)
  pytest test_simple_agent.py     # 运行指定文件
  pytest -k "add"                 # 只运行名字含 "add" 的测试
  pytest --tb=long                # 失败时显示完整 traceback
  pytest -x                       # 遇到第一个失败就停止
  pytest --cov=mycode             # 代码覆盖率 (需装 pytest-cov)

★ Ch7 的测试文件运行方式 ★
  cd code/chapter7
  pytest test_simple_agent.py -v

★ Java 对照 ★
  pytest           ≡ mvn test / gradle test
  test_xxx()       ≡ @Test public void xxx()
  assert x == y    ≡ assertEquals(y, x)
  @pytest.fixture  ≡ @BeforeEach
  @parametrize     ≡ @ParameterizedTest
  pytest.raises    ≡ assertThrows(...)
""")


# ============================================================
# 清理测试文件
# ============================================================
import os
if os.path.exists("test_with.txt"):
    os.remove("test_with.txt")
    print("已清理 test_with.txt")


print("\n" + "=" * 60)
print("✅ W2 语法收尾完成!")
print("做完 w2_03 (async/dataclass) + w2_04 (with/pytest)")
print("Python 语法阶段就全部结束了, 明天进 Ch1!")
print("=" * 60)
