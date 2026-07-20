---
name: clawd-desktop-pet-architecture
description: 从 clawd-on-desk (5.5k⭐) 学到的桌宠架构模式
metadata:
  type: reference
---

**来源：** [clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk) (5.5k⭐) — 像素桌宠，支持 Reasonix CLI

**核心架构模式：**
- **状态机 + 动画系统 + 主题系统** 三层分离
- 状态映射：idle → thinking → working → happy → error → sleeping
- 通过 command hooks 监听 AI agent 状态（SessionStart, ToolUse, TaskComplete, Error）
- 主题系统：每个主题包含 idle.svg + 7 个 GIF/APNG + theme.json
- 支持自定义主题导入（兼容 Codex Pet 包）
- SVG 眼动追踪（idle 状态）

**如何应用于 Dropout Bear 桌宠：**
- 参考 clawd-on-desk 的 `agents/` 目录中的 Reasonix hook 实现
- 使用 SVG 动画替代帧 PNG 序列以减少体积
- 实现状态映射 + 事件监听的双向通信
- 添加主题导入功能，让用户可自定义外观

**Why:** clawd-on-desk 与你的 [reasonix-dropout-bear-pet](reasonix-dropout-bear-pet.md) 桌宠项目目标完全一致，其架构经过 5.5k⭐ 验证
