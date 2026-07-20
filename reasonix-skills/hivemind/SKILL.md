---
name: hivemind
description: 搜索 Banodoco Discord 社区的 AI 视频/图像生成最佳实践。查询 Wan、ComfyUI、LTX 等工具的社区经验
---

# Hivemind — AI 视频/图像生成社区知识搜索

从 [banodoco/hivemind](https://github.com/banodoco/hivemind) (50⭐) 学到的技能。

## 能力

搜索 Banodoco Discord 社区的公开消息存档，获取 AI 视频/图像生成的最佳实践、工作流、提示词技巧。

## 使用方式

当用户问 "Banodoco 上有没有关于...的最佳实践"、"社区怎么解决...问题" 时触发。

### API 端点

```bash
# 搜索统一信息源（消息+资源+精华）
curl -s "https://ujlwuvkrxlvoswwkerdf.supabase.co/rest/v1/unified_feed?select=kind,title,body,author&body=ilike.*关键词*&limit=10" \
  -H "apikey: sb_publishable_O38oPBafrBoFrpi_rlWJvA_UJrulFsx"
```

### 高频搜索渠道

| 频道 | 内容 |
|------|------|
| wan_chatter | Wan 视频生成讨论 |
| wan_comfyui | Wan + ComfyUI 工作流 |
| ltx_chatter | LTX 模型讨论 |
| comfyui | ComfyUI 通用 |
| daily_summaries | 每日精华摘要 |

### 搜索模式

```bash
# 关键词搜索
...body=ilike.*Wan Animate best practices*

# 按频道过滤
...channel=in.(wan_chatter,wan_comfyui)&body=ilike.*SCAIL*

# 按作者权重（Kijai, Ablejones, djbfilmz 等是社区专家）
...author=ilike.*Kijai*
```

## 适用场景

- Wan Animate / Wan 视频生成最佳实践
- ComfyUI 工作流
- SCAIL vs Wan Animate 对比
- LTX 模型参数推荐
- 视频生成提示词技巧
