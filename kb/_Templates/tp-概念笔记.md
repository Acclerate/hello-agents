<%*
let title = tp.file.title;
let category = await tp.system.suggester(
	["基础","构建","高级","综合案例","毕业设计","避坑"],
	["基础","构建","高级","综合案例","毕业设计","避坑"],
	false,
	"选择所属篇章"
);
let difficulty = await tp.system.suggester(
	["⭐ 入门","⭐⭐ 重要","⭐⭐⭐ 高频难点","⭐⭐⭐⭐ 压轴"],
	["1","2","3","4"],
	false,
	"选择难度"
);
-%>
---
type: 概念
title: "<% title %>"
category: <% category %>
difficulty: <% difficulty %>
status: 未复习
created: <% tp.date.now("YYYY-MM-DD") %>
review_dates: []
tags:
  - ha
  - ha/<% category %>
aliases: []
---

# <% title %>

> [!info] 一句话定义
> 

## 🎯 核心概念

### 是什么
- 

### 为什么重要
- 

### 在书中的位置
| 章 | 位置 | 说明 |
| --- | --- | --- |
|  | [[第01章 · 初识智能体\|]] |  |

## ⚠️ 易错点 & 陷阱
- ❌ 常见误解：
- ✅ 正确理解：

## 🔗 关联知识
- 上位概念：[[]]
- 对比区分：[[]]

## 🃏 闪卡（Spaced Repetition）
#flashcards/ha/<% category %>

<% title %>是什么？::

## 📅 复习记录
- <% tp.date.now("YYYY-MM-DD") %>：初次学习
