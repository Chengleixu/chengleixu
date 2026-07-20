---
name: pixverse-bailian-video-standard
description: 阿里云百炼视频生成标准 + 免费额度用尽自动切换模型策略
metadata:
  type: project
---

## 视频生成标准 + 自动切换模型策略

### 重点：必须使用有免费额度的模型版本
`wan2.7-i2v`（无日期后缀）**没有免费额度**，切勿使用。

### 免费额度自动切换序列（用完一个自动切下一个）

| 顺序 | 模型 | 剩余额度 | 类型 |
|:---:|------|:--------:|:----:|
| ① | `wan2.7-i2v-2026-04-25` | **50秒** 🟢 | 图生视频（首选） |
| ② | `wan2.7-t2v` | **50秒** 🟢 | 文生视频 |
| ③ | `wan2.6-t2v` | **29秒** 🟢 | 文生视频 |
| ④ | `wan2.2-t2v-plus` | **50秒** 🟢 | 文生视频 |
| ⑤ | `happyhorse-1.1-t2v` | **10秒** 🟢 | 文生视频 |
| ⑥ | `wanx2.1-t2v-turbo` | **200秒** 🟢 | 兜底 |

### 角色特征
**🟣 粉色：** 粉红+白肚皮、大头大黑眼+浅绿眼白、无鼻无耳、小直线嘴、黑色短手脚
**🟡 黄色：** 黄色、大耳（粉色内侧）、细长尾巴、黑色小眼+浅绿眼白、无鼻、黄色短手脚

### CLI 命令模板
```powershell
# 图生视频（优先用这个）
bl video generate --model wan2.7-i2v-2026-04-25 --image <本地图> --prompt "<完整故事>" --resolution 720P --ratio 16:9 --duration <秒> --watermark false

# 文生视频（备用）
bl video generate --model wan2.7-t2v --prompt "<完整故事>" --resolution 720P --ratio 16:9 --duration <秒> --watermark false
```

### 每次生成前先查额度
```powershell
bl usage free --output json | ConvertFrom-Json | Where-Object {$_.type -eq "Vision" -and $_.remaining -gt 0}
```

**Why:** 用户要求免费额度用完后自动切换到下一个还有免费额度的模型，避免按量扣费。
**How to apply:** 每次生成前先检查免费额度，用完当前模型的额度后按顺序切换到下一个模型。
