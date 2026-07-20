---
name: character-video-pipeline
description: 角色视频生成流水线 — 从角色设定/参考图到多镜头剧情的完整工作流（适配 Agnes AI + 阿里云百炼）
run_as: subagent
allowed_tools:
  - bash
  - write_file
  - read_file
  - web_fetch
---

# 角色视频生成流水线

受 SamurAIGPT/Generative-Media-Skills 的 Recipe Pack 模式启发，专为你的双角色（粉色+黄色虚构生物）视频创作设计。

## 工作流概述

```
角色设定 → 生成参考图 → 编写剧本/分镜 → 逐镜头图生视频 → 筛选最佳 → 合成+配音
```

## 步骤 1：角色一致性检查

每次生成前，读取角色设定记忆并确认：
- [character-library-v2](character-library-v2.md) — 角色精确特征
- [character-library-v3](character-library-v3.md) — 用户原图参考
- [video-character-identity](video-character-identity.md) — 黄色角色非大象
- [video-character-traits](video-character-traits.md) — 粉无尾/黄无鼻

**将参考图和 prompt 传给 Agnes AI 或 阿里云百炼前，必须显式声明这些特征约束。**

## 步骤 2：剧本与分镜

按以下格式编写剧本：

```
场景 N: [场景描述]
时长: [秒数]
角色: [粉色/黄色/双角色]
动作: [具体动作描述]
镜头: [全景/中景/特写/推拉摇移]
情绪: [欢乐/好奇/惊讶/互动]
参考图: [路径]
```

## 步骤 3：图生视频

参考阿里云百炼最佳实践：

```bash
# 阿里云百炼图生视频
bailian video create --model wan-i2v-plus \
  --image-url "<参考图URL>" \
  --prompt "<动作描述>" \
  --duration 5
```

**关键约束：**
- 避免生成额外角色（模型常会自作主张添加新角色）
- 粉色角色不能有尾巴
- 黄色角色不能有鼻子/长鼻子
- 首帧必须包含角色主体

## 步骤 4：筛选与迭代

生成后检查：
1. 角色数量是否正确（不应多出角色）
2. 角色特征是否准确（粉色无尾/黄色无鼻）
3. 动作是否符合预期
4. 画面质量是否可用

## 步骤 5：合成

使用阿里云百炼的视频合成能力或 `ffmpeg` 进行：
- 镜头拼接
- TTS 配音（阿里云百炼 TTS）
- 字幕叠加
