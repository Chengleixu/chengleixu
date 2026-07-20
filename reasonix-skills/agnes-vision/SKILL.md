---
name: agnes-vision
description: 通过 Agnes AI API 读取和理解图片内容，支持本地图片和图片URL
---

---
name: agnes-vision
description: "通过 Agnes AI API 读取和理解图片内容，支持本地图片和图片 URL"
tags:
  - agnes
  - vision
  - image-understanding
  - multimodal
---

# Agnes Vision Skill

当用户要求**读取图片内容、描述图片、分析截图、OCR 识别图片文字、视觉问答**时，使用此 skill。

## 前置条件

- 需要已配置 `AGNES_API_KEY` 环境变量
- 需要已安装 `agnes-ai-cli`（用于上传本地图片）

## 检查 AGNES_API_KEY

```bash
if (-not $env:AGNES_API_KEY) {
    Write-Error "AGNES_API_KEY 未配置。请先配置 API Key。"
    return
}
```

## 处理流程

### 步骤 1：获取图片的公开 URL

**情况 A：用户提供了图片 URL（http/https）**
- 直接使用该 URL

**情况 B：用户提供了本地图片路径**
- 先确认文件存在
- 使用 `agnes-ai-cli` 上传到临时公网 URL：

```bash
npx -y agnes-ai-cli@^0.1.0 media url "<本地图片路径>" --json
```

- 从返回结果中提取 `url` 字段

### 步骤 2：调用 Agnes API 进行图片理解

使用 `agnes-2.0-flash` 模型，通过 `/v1/chat/completions` 端点发送请求。

Base URL: `https://apihub.agnes-ai.com/v1`

请求格式（OpenAI 兼容）：

```json
{
  "model": "agnes-2.0-flash",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "<用户的提问>"},
        {"type": "image_url", "image_url": {"url": "<图片公网URL>"}}
      ]
    }
  ]
}
```

### 步骤 3：返回结果

将模型的回答返回给用户。注意：
- 图片理解请求可能需要 30-180 秒处理时间
- 建议使用 `--max-time 300` 设置超时
- 使用后台任务运行以避免阻塞

## 常见提示词模板

| 任务类型 | 推荐提示词 |
|---------|-----------|
| 通用描述 | "请详细描述这张图片的内容，包括所有可见元素、颜色、布局等" |
| 截图分析 | "分析这张截图中的界面元素、布局和功能" |
| OCR/文字识别 | "请提取这张图片中的所有文字内容" |
| 视觉问答 | "回答关于这张图片的问题：[具体问题]" |

## 注意事项

- 图片 URL 必须是公开可访问的
- 临时上传的图片 URL 有时效性，请尽快使用
- 图片理解响应较慢（通常 30-120 秒），请耐心等待
- 当前 API 免费使用，但官方可能随时调整定价策略
- 始终使用 `sk-` 开头的 API Key 进行认证
