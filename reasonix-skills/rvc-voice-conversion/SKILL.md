---
name: rvc-voice-conversion
description: RVC 声音转换 — 用本地训练好的音色模型转换任何人声。配合 TTS 使用可实现任意角色配音
---

# RVC 声音转换工具

使用本地的 [RVC WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) 进行声音转换。

## 位置

```
D:\RVC20240604Nvidia\
├── runtime\python.exe      ← 专用 Python 运行时
├── tools\infer_cli.py      ← 单文件推理
├── tools\infer_batch_rvc.py ← 批量推理
├── assets\weights\          ← 模型文件 (.pth)
└── logs\                    ← 索引文件 (.index)
```

## 可用的音色模型（23 个）

| 模型名 | 文件 |
|--------|------|
| aiyi | `assets/weights/aiyi.pth` |
| chuhua | `assets/weights/chuhua.pth` |
| deng | `assets/weights/deng.pth` |
| dingzhen_e10~e40 | `assets/weights/dingzhen_e*.pth` |
| donghaidihuang | `assets/weights/donghaidihuang.pth` |
| guanguanV1 | `assets/weights/guanguanV1.pth` |
| keruanV1 | `assets/weights/keruanV1.pth` |
| kikiV1 | `assets/weights/kikiV1.pth` |
| laoda | `assets/weights/laoda.pth` |
| lenai | `assets/weights/lenai.pth` |
| lixi | `assets/weights/lixi.pth` |
| manbo / manbo_2_e100 | `assets/weights/manbo*.pth` |
| nuoyemu | `assets/weights/nuoyemu.pth` |
| sushi | `assets/weights/sushi.pth` |
| tomori_boukaru | `assets/weights/tomori_boukaru.pth` |
| xiangzi | `assets/weights/xiangzi.pth` |
| ykn-test | `assets/weights/ykn-test*.pth` |
| youzhanv2-xi | `assets/weights/youzhanv2-xi.pth` |

## 单文件声音转换

```bash
cd D:\RVC20240604Nvidia
runtime\python.exe tools\infer_cli.py ^
  --model_name <模型名> ^
  --input_path <输入音频.wav> ^
  --opt_path <输出音频.wav> ^
  --index_path logs/<索引文件.index> ^
  --f0method harvest ^
  --index_rate 0.66
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--f0up_key` | 0 | 音高偏移（半音），正数升高，负数降低 |
| `--input_path` | 必填 | 输入音频路径 (.wav) |
| `--index_path` | 必填 | 特征索引路径 |
| `--f0method` | harvest | 基音提取算法：`harvest` 或 `pm` |
| `--opt_path` | 必填 | 输出音频路径 |
| `--model_name` | 必填 | 模型名（去掉 .pth 后缀） |
| `--index_rate` | 0.66 | 索引检索比例（0-1） |
| `--filter_radius` | 3 | 中值滤波半径（>=3 启用） |
| `--resample_sr` | 0 | 重采样率（0 为不重采样） |
| `--rms_mix_rate` | 1 | 音量混合比例（0-1） |
| `--protect` | 0.33 | 辅音保护系数（0-0.5） |

## 批量处理

```bash
cd D:\RVC20240604Nvidia
runtime\python.exe tools\infer_batch_rvc.py ^
  --model_name <模型名> ^
  --input_path <输入目录> ^
  --opt_path <输出目录> ^
  --index_path logs/<索引.index>
```

## 与视频工作流集成

典型的配音流程：
1. 编写剧本 → 生成 TTS 音频（阿里云百炼 TTS 或 Agnes AI）
2. 用 RVC 将 TTS 音频转换为目标角色的音色
3. 将转换后的音频与视频合成

```bash
# 步骤 1: 生成 TTS
# (使用阿里云百炼或 Agnes AI)

# 步骤 2: RVC 声音转换
cd D:\RVC20240604Nvidia
runtime\python.exe tools\infer_cli.py ^
  --model_name dingzhen_e40 ^
  --input_path "C:\temp\tts_output.wav" ^
  --opt_path "C:\temp\converted_voice.wav" ^
  --index_path logs\added_IVF256_Flat_nprobe_1_tomori_boukaru_v2.index ^
  --f0method harvest ^
  --index_rate 0.66

# 步骤 3: 合成到视频
ffmpeg -i video.mp4 -i converted_voice.wav -c:v copy -c:a aac output.mp4
```
