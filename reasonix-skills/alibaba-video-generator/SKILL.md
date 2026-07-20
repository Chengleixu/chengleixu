---
name: alibaba-video-generator
description: 阿里云百炼视频生成工作流：图生视频/文生视频+TTS配音+自动切换免费模型+上传可播放链接
---

# 阿里云百炼视频生成 Skill

当你需要生成 AI 视频时，按此流程执行。

## 前置条件
- 阿里云百炼 CLI (`bl`) 已安装
- API Key 已配置（`bl auth login`）
- 双角色参考图位于 `.reasonix/attachments/clipboard-20260719-161058.273660-000014.png`

## 角色特征（Prompt 中必须包含）

**粉色大角色：** "pink round character with white belly, no ears, no nose, small straight mouth, black hands and feet"
**黄色小角色：** "yellow cute creature with big ears pink inside, long thin tail, no nose"

## 步骤

### 1. 查免费额度
```powershell
bl usage free --output json | ConvertFrom-Json | Where-Object {$_.type -eq "Vision" -and $_.remaining -gt 0} | Sort-Object remaining -Descending
```

### 2. 按优先级选模型（用完自动切下一个）
| 优先级 | 模型 | 剩余额度 | 类型 |
|:---:|------|:--------:|:----:|
| 1 | `wan2.7-i2v-2026-04-25` | 50秒 | 图生视频（首选） |
| 2 | `wan2.7-t2v` | 50秒 | 文生视频 |
| 3 | `wan2.6-t2v` | 29秒 | 文生视频 |
| 4 | `wan2.2-t2v-plus` | 50秒 | 文生视频 |
| 5 | `happyhorse-1.1-t2v` | 10秒 | 兜底 |

### 3. 生成视频
```powershell
# 图生视频（优先）
bl video generate --model <模型ID> --image "参考图路径" --prompt "<完整故事描述>" --resolution 720P --ratio 16:9 --duration <秒> --watermark false --async --output json

# 获取task_id后轮询
bl video task get --task-id <task_id> --output json
```

### 4. 配音（可选）
```powershell
# 用 CosyVoice TTS（免费10000秒）
bl speech synthesize --text "<配音稿>" --voice longanyang --language zh --rate 1.1 --format mp3 --out voiceover.mp3

# 合成到视频
ffmpeg -i video.mp4 -i voiceover.mp3 -filter_complex "[1:a]volume=1.2[a1]" -map 0:v -map "[a1]" -c:v copy -c:a aac -shortest output.mp4
```

### 5. 上传可播放链接
```powershell
npx -y agnes-ai-cli@^0.1.0 media url output.mp4 --json
```

### 6. 压缩（可选，文件大时）
```powershell
ffmpeg -i output.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 64k small.mp4 -y
```

## 注意事项
- **切勿使用 `wan2.7-i2v`（无日期后缀）**，它没有免费额度
- 每次生成前必须查剩余额度
- 配音稿控制在12-15秒（约60-80字）
- 推荐声音：`longanyang`（阳光大男孩）/ `longhua_v3`（元气甜美女）
