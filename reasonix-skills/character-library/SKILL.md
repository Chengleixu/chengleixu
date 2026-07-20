---
name: character-library
description: 角色素材库：记忆粉色和黄色两个卡通角色的精确特征、参考图和生成模板
---

# 角色素材库

## 🟣 粉色角色

### 外貌特征
- 粉红色身体，腹部有一块**白色大椭圆肚皮**
- **大圆头**，面部简单
- **大圆眼**：浅绿色虹膜 + 黑色瞳孔
- 小**水平裂缝嘴**（一条横线）
- **无鼻子、无耳朵**
- **短粗四肢**，**深灰色手套状手脚**（无手指脚趾）
- 整体圆润，3D卡通风格，光滑哑光质感

### 参考图
本地路径：`.reasonix\attachments\clipboard-20260720-111909.157790-000002.jpg`
在线链接：`https://litter.catbox.moe/9ddj5g.jpg`

### Prompt 关键词
```
pink round character, large white oval belly, big round head, 
big round eyes with light green iris and black pupil, 
small horizontal line mouth, no nose, no ears, 
short thick arms, short thick legs, 
dark gray rounded hands and feet like gloves, 
minimalist 3D cartoon style, smooth matte texture
```

---

## 🟡 黄色角色

### 外貌特征
- 全身整体为**黄色**
- 体型紧凑圆润
- **大圆耳朵**（内侧橙色/粉色）
- 有**细长尾巴**
- **无鼻子**
- 眼睛较小
- 短四肢
- 3D卡通风格

### 参考图
本地路径：`.reasonix\attachments\clipboard-20260719-161058.273660-000014.png`

### Prompt 关键词
```
yellow cute round creature, big round ears with orange pink inside, 
long thin tail, compact round body, no nose, 
short limbs, 3D cartoon style, smooth rendering
```

---

## 视频生成模板

### 阿里云百炼 (wan2.7-i2v-2026-04-25)
```powershell
bl video generate --model wan2.7-i2v-2026-04-25 `
  --image "参考图路径" `
  --prompt "故事描述 + [粉色角色关键词] + [黄色角色关键词]" `
  --resolution 720P --ratio 16:9 --duration 5 --watermark false
```

### 负面 prompt
```
ugly, deformed, blurry, bad anatomy, extra limbs, 
signature, watermark, text, messy, noisy
```
