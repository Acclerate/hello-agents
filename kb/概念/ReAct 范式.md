---
title: ReAct 范式
aliases:
  - ReAct
  - Reasoning and Acting
type: 概念
category: 构建
difficulty: 2
status: 未复习
created: 2026-08-28
review_dates: []
tags:
  - ha
  - ha/构建
---

# ReAct 范式

> [!info] 一句话定义
> 让 LLM 交替进行**推理（Thought）**与**行动（Action）**，并把行动结果（Observation）回填到上下文继续推理，循环直至完成任务——现代智能体的默认执行骨架。

## 🎯 核心概念

### 是什么
- 一个循环：**Thought（下一步该做什么、为什么）→ Action（调用工具/给指令）→ Observation（工具结果写回上下文）**
- 推理链与工具调用交织：边想边做，用真实反馈修正路线，而非一次性输出全盘计划
- 停止条件由 LLM 自己判断（给出最终答案或达到最大步数）

### 为什么重要
- 它是 Agent 与 Chatbot 的分水岭：**有了行动闭环才叫智能体**
- 后续所有框架（LangGraph/AutoGen/HelloAgents）的执行内核都是 ReAct 的工程化封装
- 调试 Agent 行为的基本单位就是一轮 Thought-Action-Observation

### 在书中的位置

| 章 | 位置 | 说明 |
| --- | --- | --- |
| 4 | [[第04章 · 智能体经典范式构建]] · [[实验 4-1 · ReAct 范式实现]] | 手写 ReAct，理解裸循环 |
| 6 | [[第06章 · 框架开发实践]] | 各框架对 ReAct 的封装对比 |
| 7 | [[第07章 · 构建你的Agent框架]] · [[实验 7-3 · ReAct 智能体框架化]] | 把 ReAct 收编为框架类 |
| 14 | [[第14章 · 自动化深度研究智能体]] · [[项目 14-1 · 自动化深度研究智能体]] | DeepResearch 的研究循环 |

## ⚠️ 易错点 & 陷阱
- ❌ 常见误解：ReAct = "能调工具的聊天机器人"
- ✅ 正确理解：核心在**循环 + 反馈修正**——Observation 必须真实回填，且要有停止条件，否则死循环或提前摊牌
- ❌ 输出格式不锁死（Action 无法解析）是手写版最常见故障；参考 [[PITFALLS-GUIDE]] 第四篇

## 🔗 关联知识
- 对比区分：Plan-and-Solve（先全局计划再执行）、Reflection（对输出自我批评）
- 依赖：[[Token 计量]]（轨迹越长上下文越贵）· [[MCP]]（Action 的标准化通道）

## 🃏 闪卡（Spaced Repetition）
#flashcards/ha/构建

ReAct 循环的三段是什么？::Thought → Action → Observation；推理决定行动，观察结果回填修正推理

ReAct 与 Plan-and-Solve 的适用差异？::ReAct 边走边看适合探索型任务；Plan-and-Solve 先出全局计划适合步骤确定的复杂任务，代价是计划可能过时

为什么说 ReAct 是"框架之母"？::主流框架的 Agent 执行内核本质都是 ReAct 循环 + 状态管理 + 工具分发的工程封装
