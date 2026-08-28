---
title: 第07章 · 构建你的Agent框架
chapter: 7
type: 章节
category: 构建
difficulty: 3
status: 未复习
created: 2026-08-28
review_dates: []
tags:
  - ha
  - ha/构建
---

# 第07章 · 构建你的Agent框架

> [!abstract] 一句话核心
> 从零造轮子：HelloAgents 框架 = LLM 客户端封装 + Agent 基类与三大范式实现 + 统一工具系统 + 测试驱动，亲手打通"用轮子"到"造轮子"。

## 本章小节

- 7.1 框架整体架构设计
- 7.2 HelloAgentsLLM扩展
- 7.3 框架接口实现
- 7.4 Agent范式的框架化实现
- 7.5 工具系统

## 阅读入口

- 📖 [[第七章 构建你的Agent框架|第 7 章正文]]
- 📦 上游框架仓库：github.com/jjyaoao/helloagents（V1.0.0）

## 配套实验

| 编号 | 实验 | 说明 |
| --- | --- | --- |
| 7-1 | [[实验 7-1 · LLM 客户端封装\|my_llm]] | 统一的 LLM 调用层（流式、多模型） |
| 7-2 | [[实验 7-2 · 最简智能体 SimpleAgent\|my_simple_agent]] | 最小闭环：提示 → LLM → 输出 |
| 7-3 | [[实验 7-3 · ReAct 智能体框架化\|my_react_agent]] | 把第 4 章手写 ReAct 收编为框架类 |
| 7-4 | [[实验 7-4 · 工具开发：计算器与高级搜索\|工具开发]] | 计算器 + 高级搜索两个工具的接口实现 |
| 7-5 | [[实验 7-5 · 主程序与测试验收\|my_main + tests]] | my_main 入口与 pytest 测试全家桶 |

## 相关概念

[[ReAct 范式]] · [[Token 计量]]

← [[第06章 · 框架开发实践|上一章]] · [[第08章 · 记忆与检索|下一章 →]]

## 🃏 闪卡（Spaced Repetition）

#flashcards/ha/构建

自研框架的核心分层？::LLM 客户端封装 → Agent 基类/范式实现 → 工具系统 → 主程序与测试

工具系统的关键抽象是什么？::统一 Tool 接口（名称/描述/参数 schema/执行函数），让 LLM 通过 schema 知道怎么调用

框架化 ReAct 与手写版的差别？::把循环、上下文管理、工具分发下沉到基类，范式只保留决策逻辑，可复用可测试
