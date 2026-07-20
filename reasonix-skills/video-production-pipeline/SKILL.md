---
name: video-production-pipeline
description: 8 阶段视频制作管线 — 从需求到成片的完整工作流，适配 Agnes AI + 阿里云百炼
run_as: subagent
---

# 视频制作管线

受 [gooseworks-ai/goose-video](https://github.com/gooseworks-ai/goose-video) 的 8 阶段管线模式启发。

## 工作流概览

```
需求采集 → 参考帧生成 → 配音稿+TTS → 关键帧 → 逐镜头生成 → 结尾卡 → 配乐 → 合成
```

## 阶段 1：需求采集（Intake）

收集：
- **品牌/主题** — 视频主题是什么
- **核心信息** — 要传达什么
- **目标受众** — 给谁看
- **时长** — 目标时长（秒）
- **参考素材** — 参考图/视频链接

## 阶段 2：参考帧生成（Anchors）

使用 Agnes AI 或 阿里云百炼图生图生成场景锚点图：
- 角色参考图（保持角色一致性）
- 场景背景图
- 关键道具/物品图

## 阶段 3：配音稿+TTS（Voiceover）

1. 编写配音脚本
2. 使用 TTS 生成配音（阿里云百炼 TTS 或 ElevenLabs）
3. 导出配音音频文件

## 阶段 4：关键帧（Keyframes）

每个场景生成 1-2 张关键帧，描述构图、角色位置、镜头角度。

## 阶段 5：逐镜头生成（Clips）

每个镜头使用图生视频（i2v）生成：
```bash
# 阿里云百炼
bailian video create --model wan-i2v-plus \
  --image-url "<关键帧URL>" \
  --prompt "<动作描述>" \
  --duration 5
```

## 阶段 6：结尾卡（End Card）

生成品牌结尾画面（3-5 秒静帧或动画）。

## 阶段 7：配乐（Music）

生成或选择合适的背景音乐。

## 阶段 8：合成（Compose）

使用 ffmpeg 合成最终视频：
- 拼接各片段
- 叠加配音
- 添加背景音乐
- 叠加字幕（可选）
- 输出最终文件

> **每阶段结束后暂停，让用户审核后再进入下一阶段。** 避免为已不可用的前置阶段付费。
