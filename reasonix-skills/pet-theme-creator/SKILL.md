---
name: pet-theme-creator
description: 桌宠主题创建指南 — 受 clawd-on-desk 架构启发，为 Dropout Bear 桌宠创建自定义主题和动画
---

# 桌宠主题创建指南

从 [clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk) (5.5k⭐) 学到的桌宠架构模式。

## 核心概念

一个桌宠 = 状态机 + 动画系统 + 主题系统

### 状态映射

| 状态 | 触发条件 | 动画 |
|------|---------|------|
| idle | 空闲 | 轻微浮动/眨眼 |
| thinking | AI agent 正在思考 | 出现思考气泡 |
| working | 工具执行中/编码中 | 快速敲键盘 |
| happy | 任务完成 | 庆祝动作 |
| error | 出错/失败 | 沮丧表情 |
| sleeping | 无操作超时 | 闭眼/趴下 |

### 主题结构

```
themes/<name>/
├── idle.svg          # 待机（带眼动追踪，SVG）
├── thinking.gif      # 思考
├── working.gif       # 工作
├── happy.gif         # 开心
├── error.gif         # 错误
├── sleeping.gif      # 睡眠
└── theme.json        # 主题配置
```

### 与 AI Agent 集成

clawd-on-desk 通过 command hooks 监听 AI agent 状态：
- **SessionStart** → idle/thinking
- **ToolUse** → working  
- **TaskComplete** → happy
- **Error** → error

## 应用到 Dropout Bear

你的桌宠项目 (`C:\Users\cheng\AppData\Roaming\reasonix\global-workspace\reasonix-pet`) 可以：
1. 参考 clawd-on-desk 的状态映射系统
2. 使用 SVG 动画替代帧序列（更轻量）
3. 添加 Reasonix CLI 状态监听 hook
4. 实现自定义主题导入功能
