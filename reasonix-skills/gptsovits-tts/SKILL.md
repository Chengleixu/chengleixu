---
name: gptsovits-tts
description: GPT-SoVITS 语音合成 — 从文本生成带参考音色的语音，支持中文/英文/日文等多语言，可用作视频配音
---

# GPT-SoVITS 语音合成

使用本地的 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) v2Pro 进行文本到语音合成和音色克隆。

## 位置

```
F:\GPT-SoVITS-v2pro-20250604-nvidia50\
├── api_v2.py              ← HTTP API (推荐，FastAPI)
├── api.py                 ← HTTP API (v1)
├── go-webui.bat           ← Web 界面启动
├── go-webui.ps1           ← PowerShell 启动
├── batch_inference.py     ← 批量推理
├── runtime\python.exe     ← 专用 Python 运行时
├── GPT_SoVITS\configs\    ← 配置文件
└── GPT_SoVITS\pretrained_models\ ← 预训练模型
```

## 可用模型版本

| 版本 | GPT 模型 | SoVITS 模型 |
|------|---------|-------------|
| v2 | `s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt` | `s2G2333k.pth` |
| v2Pro | `s1v3.ckpt` | `v2Pro/s2Gv2Pro.pth` |
| v4 | `s1v3.ckpt` | `gsv-v4-pretrained/s2Gv4.pth` |

## 方式一：启动 API 服务（推荐）

```powershell
cd F:\GPT-SoVITS-v2pro-20250604-nvidia50
runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
```

### 调用 TTS

```bash
# GET 方式（快速测试）
curl "http://127.0.0.1:9880/tts?text=你好世界&text_lang=zh&ref_audio_path=参考音频.wav&prompt_lang=zh&prompt_text=参考音频的文字内容"

# POST 方式（推荐）
curl -X POST "http://127.0.0.1:9880/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "要合成的文本",
    "text_lang": "zh",
    "ref_audio_path": "参考音频.wav",
    "prompt_text": "参考音频对应的文字",
    "prompt_lang": "zh",
    "top_k": 5,
    "top_p": 1,
    "temperature": 1,
    "text_split_method": "cut5",
    "media_type": "wav"
  }' --output output.wav
```

### API 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `text` | ✅ | 要合成的文本 |
| `text_lang` | ✅ | 文本语言（zh/en/ja/kr/yue） |
| `ref_audio_path` | ✅ | 参考音频路径（用于音色克隆） |
| `prompt_text` | ❌ | 参考音频对应的文本 |
| `prompt_lang` | ✅ | 参考音频的语言 |
| `media_type` | ❌ | 输出格式（wav/ogg/aac） |
| `temperature` | ❌ | 采样温度（默认1） |
| `streaming_mode` | ❌ | 是否流式返回 |

### 切换模型

```bash
# 切换 GPT 模型
curl "http://127.0.0.1:9880/set_gpt_weights?weights_path=GPT_SoVITS/pretrained_models/s1v3.ckpt"

# 切换 SoVITS 模型
curl "http://127.0.0.1:9880/set_sovits_weights?weights_path=GPT_SoVITS/pretrained_models/v2Pro/s2Gv2Pro.pth"
```

## 方式二：直接 WebUI

```powershell
cd F:\GPT-SoVITS-v2pro-20250604-nvidia50
.\go-webui.bat
```

## 方式三：批量推理

```powershell
cd F:\GPT-SoVITS-v2pro-20250604-nvidia50
runtime\python.exe batch_inference.py
```

## 与 RVC + 视频工作流集成

推荐的配音流程：

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ GPT-SoVITS  │    │     RVC      │    │    FFmpeg   │
│ 文本→语音   │───→│ 音色精调     │───→│ 合成到视频  │
│ (参考音色)  │    │ (可选增强)   │    │             │
└─────────────┘    └──────────────┘    └─────────────┘
```

### 完整示例：给角色视频配指定音色

```powershell
# 1. GPT-SoVITS：用参考音频生成基础语音
curl -X POST "http://127.0.0.1:9880/tts" ^
  -H "Content-Type: application/json" ^
  -d '{"text":"你好，我是你的小伙伴","text_lang":"zh","ref_audio_path":"F:\\GPT-SoVITS-v2pro-20250604-nvidia50\\参考音频\\角色参考.wav","prompt_text":"参考音频文字","prompt_lang":"zh"}' ^
  --output C:\temp\tts_raw.wav

# 2. RVC：转换音色（如果需要更精细控制）
cd D:\RVC20240604Nvidia
runtime\python.exe tools\infer_cli.py ^
  --model_name dingzhen_e40 ^
  --input_path C:\temp\tts_raw.wav ^
  --opt_path C:\temp\tts_converted.wav ^
  --index_path logs\added_IVF256_Flat_nprobe_1_tomori_boukaru_v2.index

# 3. 合成到视频
ffmpeg -i video.mp4 -i C:\temp\tts_converted.wav -c:v copy -c:a aac final.mp4
```
