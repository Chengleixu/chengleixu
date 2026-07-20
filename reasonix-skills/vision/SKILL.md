---
name: vision
description: 图片识别与分析 Skill — 支持本地图片和 URL，自动 base64 编码、API 调用、结果解析
version: 2.0.0
run_as: inline
allowed_tools:
  - run_command
  - read_file
---

# 多模态识图 Skill

## 能力

你是一名图像分析专家，能够：
- 识别本地图片内容（自动 base64 编码）
- 识别网络图片 URL 内容
- 提取图片中的文字 (OCR)
- 分析图表、截图等
- 多模型自动回退

## 前置条件

- Python 3.10+ 环境
- 已配置 API Key（见下方）

## 环境变量

```bash
VISION_API_KEY=<your-api-key>       # 必需 - API 密钥
VISION_API_URL=<your-endpoint>/v1/chat/completions  # 必需 - API 地址
VISION_MODEL=<首选模型名称>           # 必需 - 模型名称
VISION_FALLBACK=<备选模型名称>        # 可选 - 首选失败时回退
```

## 核心工作流

```
用户提供图片路径/URL → 解析参数 → 调用 vision_api.py → 格式化输出
```

### 调用方式

```bash
# 本地图片
python scripts/vision_api.py /path/to/image.jpg "这张图里有什么？"

# 网络图片
python scripts/vision_api.py https://example.com/photo.png "描述一下"
```

脚本返回 JSON：

```json
{
  "success": true,
  "model": "<模型名称>",
  "description": "图片描述内容...",
  "usage": {"prompt_tokens": 1000, "completion_tokens": 200, "total_tokens": 1200}
}
```

### 失败回退

脚本自动处理模型回退（首选 → 备选），失败时返回结构化错误信息。
