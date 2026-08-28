---
title: MCP
aliases:
  - Model Context Protocol
  - MCP 协议
type: 概念
category: 高级
difficulty: 3
status: 未复习
created: 2026-08-28
review_dates: []
tags:
  - ha
  - ha/高级
---

# MCP

> [!info] 一句话定义
> Model Context Protocol：智能体与工具/数据源之间的标准连接协议——把"每个工具写一次集成"变成"接入协议、处处可用"。

## 🎯 核心概念

### 是什么
- 客户端-服务器架构：MCP Host/Client ↔ MCP Server
- 三类原语：**工具（Tools，可调用函数）**、**资源（Resources，可读数据）**、**提示（Prompts，可复用模板）**
- 传输：stdio（本地进程）与 HTTP/SSE（远程服务）
- 服务器自描述：通过 schema 声明能力，客户端动态发现

### 为什么重要
- 工具生态的"USB-C"：一次封装，所有支持 MCP 的客户端都能用
- 企业落地关键：权限、审计、沙箱在协议层统一处理
- 与 A2A 互补：MCP 管 Agent↔工具，A2A 管 Agent↔Agent

### 在书中的位置

| 章 | 位置 | 说明 |
| --- | --- | --- |
| 10 | [[第10章 · 智能体通信协议]] · [[实验 10-1 · MCP 连接测试]] 等 ×15 | MCP 全线实战 + 自建天气服务器 |
| 13 | [[第13章 · 智能旅行助手]] · [[项目 13-1 · 智能旅行助手]] | 项目中集成 MCP 工具链 |
| 拓展 | [[Extra05-AgentSkills解读]] | Agent Skills 与 MCP 对比 |

## ⚠️ 易错点 & 陷阱
- ❌ 常见误解：MCP = Function Calling
- ✅ 正确理解：Function Calling 是 LLM API 层的调用格式；MCP 是应用层协议，管的是工具的发现、传输与权限
- ❌ 工具越多越好？→ 工具列表挤占上下文且降低选择准确率，按需挂载

## 🔗 关联知识
- 对比区分：[[ReAct 范式]]（Action 的执行通道）· A2A/ANP（Agent 间通信，见 [[第10章 · 智能体通信协议]]）

## 🃏 闪卡（Spaced Repetition）
#flashcards/ha/高级

MCP 的三类原语？::工具（可调用函数）、资源（可读数据）、提示（可复用模板）

MCP 与 Function Calling 的区别？::FC 是模型 API 层的调用格式；MCP 是应用层协议，标准化工具发现、传输与权限

MCP 与 A2A 的分工？::MCP 连接 Agent 与工具/数据源；A2A 连接 Agent 与 Agent（任务委托与通信）
