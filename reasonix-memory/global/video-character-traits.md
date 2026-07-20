---
name: video-character-traits
title: 两角色外貌特征：无尾巴/无鼻子
description: 粉色角色无尾巴，黄色角色无鼻子
metadata:
  type: user
---

两个角色的关键外貌特征：
- **粉色大角色**：圆润、无尾巴（no tail）、体型偏胖
- **黄色小角色**：虚构生物（非大象、无长鼻子）、**完全没有鼻子**（no nose, flat face）
- 两者都是 3D 卡通风格

**Why:** 用户反馈指出生成视频中粉色角色被添加了尾巴，黄色角色被添加了鼻子。

**How to apply:** 生成时在 prompt 中强调 "no tail"（对粉色角色）和 "no nose, flat face"（对黄色角色）；negative prompt 中加入 "tail, nose, trunk"。
