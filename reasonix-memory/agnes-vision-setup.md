---
name: agnes-vision-setup
title: Agnes AI 图片读取能力已配置
description: Agnes Vision 图片理解功能已通过 Agnes AI API 配置完成
metadata:
  type: project
---

## Agnes AI 图片读取能力

**为什么记录：** 用户已配置 Agnes AI API，获得了图片读取/理解能力。

### 已安装的 Skills

| Skill | 位置 | 用途 |
|-------|------|------|
| `agnes-ai-skill` | `.reasonix/skills/agnes-ai-skill/SKILL.md` | Agnes AI 通用（文本/图像/视频生成） |
| `agnes-vision` | `.reasonix/skills/agnes-vision/SKILL.md` | 图片读取/理解专用 skill |

### AGNES_API_KEY

- 已保存到 Windows 用户环境变量
- 当前 key: 以 `sk-ra9CRZGy...` 开头
- 创建地址：https://platform.agnes-ai.com/settings/apiKeys
- Base URL：https://apihub.agnes-ai.com/v1
- 模型：`agnes-2.0-flash`（支持图片理解）

### 如何使用

1. 调用 `agnes-vision` skill（`run_skill({name:"agnes-vision"})`）
2. 或直接调用 Agnes API：`POST /v1/chat/completions`，通过 `image_url` 传入图片
3. 本地图片先用 `npx -y agnes-ai-cli@^0.1.0 media url <路径> --json` 上传获取公网 URL

**Why:** 用户希望在所有对话中都能使用图片读取功能。
**How to apply:** 新对话加载记忆后，如果发现用户需要读取图片，优先调 `agnes-vision` skill 或直接使用上述 API 格式。
