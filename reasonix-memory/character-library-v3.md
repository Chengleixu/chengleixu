---
name: character-library-v3
description: 粉色和黄色角色的用户原图及双角色同框图
metadata:
  type: project
---

## 角色素材库（用户原图版）

### 🟣 粉色角色原图
**路径：** `.reasonix\output\ref_pink_original.jpg`

### 🟡 黄色角色原图
**路径：** `.reasonix\output\ref_yellow_original_v2.jpg`

### 🎯 双角色同框参考图
**路径：** `.reasonix\output\ref_both_original.png`

### 生成规则
所有视频生成使用阿里云百炼 `wan2.7-i2v-2026-04-25` 图生视频，以上述参考图作为输入。

**Why:** 用户提供了粉色、黄色角色各自的独立原图及双角色同框图，要求严格按原图生成。
**How to apply:** 生成视频时优先使用对应角色的原图作为 img2video 参考图。双角色同框的场景使用同框图。
