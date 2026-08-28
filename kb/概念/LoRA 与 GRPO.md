---
title: LoRA 与 GRPO
aliases:
  - LoRA
  - GRPO
  - 参数高效微调
type: 概念
category: 高级
difficulty: 4
status: 未复习
created: 2026-08-28
review_dates: []
tags:
  - ha
  - ha/高级
---

# LoRA 与 GRPO

> [!info] 一句话定义
> 消费级显卡练模型的两个关键词：**LoRA** 冻结基座、只训低秩增量，把可训练参数降 2-3 个数量级；**GRPO** 用组内相对奖励替代 critic 网络，让 RL 微调更省显存更好实现。

## 🎯 核心概念

### 是什么
- **LoRA**：权重增量 ΔW ≈ B·A（低秩分解），训练只更新 A/B；常配合 4bit 量化（QLoRA）进一步压显存
- **GRPO**（Group Relative Policy Optimization）：同一 prompt 采样一组回答，用**组内奖励均值做基线**，替代 PPO 的 value 网络
- 标准路径：SFT（模仿示范）→ RL/GRPO（按奖励优化行为）

### 为什么重要
- 让 RTX 4060 级别的显卡也能跑通"训练自己的智能体"全流程
- 奖励函数设计是 Agentic RL 的核心杠杆：奖励什么，模型就成为什么
- 岗位面试高频：GRPO vs PPO、LoRA 原理与显存账（见 [[Extra01-面试问题总结]]）

### 在书中的位置

| 章 | 位置 | 说明 |
| --- | --- | --- |
| 11 | [[第11章 · Agentic-RL]] · [[实验 11-4 · LoRA 配置]] · [[实验 11-6 · GRPO 训练]] | 数据→奖励→SFT→GRPO→评估全管线 |
| 12 | [[第12章 · 智能体性能评估]] · [[实验 11-8 · 模型评估]] | 训练效果要用基准说话 |
| 拓展 | [[Extra12-旅行助手后训练实战]] | 旅行助手的后训练实战 |

## ⚠️ 易错点 & 陷阱
- ❌ 常见误解：LoRA 让推理更便宜
- ✅ 正确理解：LoRA 只降低**训练**开销；推理仍走全参数（除非合并权重或继续量化）
- ❌ OOM 先降 batch？→ 顺序是：梯度检查点 → 量化位数 → 减序列长度/组大小，见 [[PITFALLS-GUIDE]] 第七篇显存账

## 🔗 关联知识
- 对比区分：SFT（模仿）vs GRPO（优化）；PPO（有 critic）vs GRPO（组内基线）
- 依赖：[[Token 计量]]（序列长度 ↔ 显存）

## 🃏 闪卡（Spaced Repetition）
#flashcards/ha/高级

LoRA 为什么省显存？::冻结基座只训低秩分解的增量矩阵，可训练参数量降 2-3 个数量级

GRPO 去掉了 PPO 的什么组件，靠什么替代？::去掉 value/critic 网络；用同 prompt 组内奖励均值当基线

SFT 与 RL 各自教模型什么？::SFT 教"照示范做"（模仿分布）；RL 用奖励信号优化目标行为
