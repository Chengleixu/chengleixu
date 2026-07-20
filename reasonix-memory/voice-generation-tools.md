---
name: voice-generation-tools
description: GPT-SoVITS (TTS) + RVC (声音转换) 的调用方式和视频配音工作流
metadata:
  type: reference
---

**工具位置：**
- GPT-SoVITS: `F:\GPT-SoVITS-v2pro-20250604-nvidia50\`
  - API 服务: `runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml`
  - API 端点: `POST http://127.0.0.1:9880/tts`（参数：text, text_lang, ref_audio_path, prompt_text, prompt_lang）
  - 可用模型：v2Pro（默认）, v2, v4
  - WebUI: `go-webui.bat`
- RVC: `D:\RVC20240604Nvidia\`
  - 单文件推理: `runtime\python.exe tools\infer_cli.py --model_name <模型> --input_path <输入> --opt_path <输出> --index_path <索引>`
  - 可用音色：aiyi, chuhua, deng, dingzhen_e10~e40, guanguanV1, keruanV1, kikiV1, laoda, lenai, lixi, manbo, nuoyemu, sushi, tomori_boukaru, xiangzi, ykn-test, youzhanv2-xi（23个）
  - WebUI: `go-web.bat`（端口 7897）
  - 实时变声: `go-realtime-gui.bat`

**推荐视频配音流程：**
1. GPT-SoVITS：文本 → 语音（用参考音频克隆角色音色）
2. RVC（可选）：进一步精调音色
3. FFmpeg：合成到视频

**Why:** 这两个工具互补——GPT-SoVITS 负责从文本直接生成带特定音色的语音，RVC 做语音到语音的精细转换。两者配合可为视频角色生成任意想要的配音。

**关联记忆：**
- [video-generation-lessons](video-generation-lessons.md) — 视频生成经验
- [generative-media-skills-patterns](generative-media-skills-patterns.md) — 视频工作流模式
- [clawd-desktop-pet-architecture](clawd-desktop-pet-architecture.md) — 桌宠架构
