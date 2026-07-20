---
name: mimo-skill
description: 小米 MiMo 大模型 API — 文本对话、图像理解(URL/base64)、语音识别ASR、语音合成TTS
---

# MiMo AI Skill

小米 MiMo 大模型 API 技能。支持文本对话、图像理解、语音识别 (ASR) 和语音合成 (TTS)。

## 基本信息

- **Base URL**: `https://api.xiaomimimo.com/v1`
- **Auth**: `Authorization: Bearer <MIMO_API_KEY>`
- **环境变量**: `MIMO_API_KEY`（`sk-` 开头的 key）
- **上下文窗口**: 1M tokens
- **接口格式**: OpenAI 兼容

## 可用模型

| 模型 ID | 用途 |
|---------|------|
| `mimo-v2.5` | 基础模型：文本对话 + **图像理解**（URL / base64） |
| `mimo-v2.5-pro` | 纯文本高级版（不支持图像输入） |
| `mimo-v2.5-asr` | 语音识别（音频转文字） |
| `mimo-v2.5-tts` | 语音合成（文字转语音） |
| `mimo-v2.5-tts-voiceclone` | 语音克隆 |
| `mimo-v2.5-tts-voicedesign` | 语音设计 |

## 检查 API Key

```powershell
if (-not $env:MIMO_API_KEY) {
    Write-Error "MIMO_API_KEY 未配置"
    return
}
```

## 文本对话

```powershell
curl -s -X POST "$baseUrl/chat/completions" `
  -H "Authorization: Bearer $env:MIMO_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{
    "model": "mimo-v2.5",
    "messages": [
      {"role": "user", "content": "你好"}
    ],
    "max_tokens": 1000
  }'
```

## 图像理解

支持 **图片 URL** 和 **Base64** 两种方式。

> ⚠️ 只有 `mimo-v2.5` 支持图像理解，`mimo-v2.5-pro` 不支持。

### 方式 A：图片 URL

```powershell
curl -s -X POST "$baseUrl/chat/completions" `
  -H "Authorization: Bearer $env:MIMO_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{
    "model": "mimo-v2.5",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "请描述这张图片"},
          {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
      }
    ],
    "max_tokens": 500
  }'
```

### 方式 B：Base64 编码

```powershell
curl -s -X POST "$baseUrl/chat/completions" `
  -H "Authorization: Bearer $env:MIMO_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{
    "model": "mimo-v2.5",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "描述图片内容"},
          {"type": "image_url", "image_url": {"url": "data:image/png;base64,iVBORw0KGgoAAAAN..."}}
        ]
      }
    ],
    "max_tokens": 500
  }'
```

## 语音识别 (ASR)

使用 `mimo-v2.5-asr` 模型进行语音转文字。

```powershell
curl -s -X POST "$baseUrl/audio/transcriptions" `
  -H "Authorization: Bearer $env:MIMO_API_KEY" `
  -H "Content-Type: multipart/form-data" `
  -F "model=mimo-v2.5-asr" `
  -F "file=@/path/to/audio.wav"
```

## 语音合成 (TTS)

使用 `mimo-v2.5-tts` 模型进行文字转语音。

```powershell
curl -s -X POST "$baseUrl/audio/speech" `
  -H "Authorization: Bearer $env:MIMO_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{
    "model": "mimo-v2.5-tts",
    "input": "你好，我是小米大模型",
    "voice": "xiaomi-voice"
  }' --output output.mp3
```

## 常用提示词模板（图像理解）

| 任务 | 推荐提示词 |
|------|-----------|
| 通用描述 | "请详细描述这张图片的内容" |
| 提取用于AI生成的 prompt | "Describe this image in English for use as an AI image generation prompt" |
| OCR/文字识别 | "请提取这张图片中的所有文字" |
| 视觉问答 | "回答关于这张图片的问题：[问题]" |
| 质量评估 | "评价这张图片的构图、色彩、光线、真实感，满分10分" |

## 联合使用（MiMo + 其他 AI）

MiMo 擅长图像理解，但不支持图像/视频生成。推荐与 Agnes AI / FLUX 等生成工具联合使用：

```
MiMo 看图提取描述 → 其他AI根据描述生成图片/视频
其他AI生成图片 → MiMo 审核质量
```

## 注意事项

- 图片 URL 必须是 MiMo 服务端可访问的公网地址
- Base64 图片数据会增加 token 消耗
- 响应中包含 `reasoning_content` 字段（推理链），可选择性展示
- MiMo 目前**不支持**视频理解和视频生成
- 图像理解响应通常 3-15 秒
- 当前 1M 上下文窗口适合长文档分析
