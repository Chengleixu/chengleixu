---
name: msst-audio-separation
description: MSST-WebUI 音乐源分离 — 人声/伴奏分离、去混响、降噪。比 UVR5 更先进的音频处理工具
---

# MSST-WebUI 音乐源分离工具

[MSST-WebUI](https://github.com/SUC-DriverOld/MSST-WebUI) 是 Music-Source-Separation-Training 的 WebUI，集成了最先进的音频源分离模型和 UVR。

## 位置

```
D:\AI\MSST WebUI\
├── webUI.py                  ← WebUI 启动入口
├── go-webui.bat              ← 一键启动 WebUI
├── inference/msst_infer.py   ← Python 推理接口
├── pretrain/
│   ├── vocal_models/         ← 人声提取模型
│   ├── single_stem_models/   ← 单轨处理（去混响/降噪）
│   ├── multi_stem_models/    ← 多轨分离
│   └── VR_Models/            ← UVR 兼容模型
├── configs/                  ← 模型配置文件
├── input/                    ← 输入目录
├── results/                  ← 输出目录
└── workenv/python.exe        ← 专用 Python 运行时
```

## 可用模型

### 人声分离 (vocal_models)

| 模型文件 | 用途 |
|---------|------|
| `mel_band_roformer_vocals_becruily.ckpt` | 高质量人声提取 |
| `model_mel_band_roformer_karaoke_*.ckpt` | 卡拉OK人声提取 |
| `melband_roformer_inst_v2.ckpt` | 伴奏提取 |
| `big_beta5e.ckpt` | 备用人声模型 |
| `inst_v1e.ckpt` | 备用伴奏模型 |

### 音频处理 (single_stem_models)

| 模型文件 | 用途 |
|---------|------|
| `denoise_mel_band_roformer_*.ckpt` | 降噪 |
| `dereverb_mel_band_roformer_*.ckpt` | 去混响 |
| `de_big_reverb_mbr_ep_362.ckpt` | 去大混响 |
| `dereverb_echo_mbr_fused_*.ckpt` | 去混响+回声 |

## 启动 WebUI

```powershell
cd D:\AI\MSST WebUI
.\go-webui.bat
```

## Python 调用（批量处理）

```python
from inference.msst_infer import MSSeparator

# 人声分离
separator = MSSeparator(
    model_type="mel_band_roformer",
    config_path="configs/config_vocals_bs_roformer.yaml",
    model_path="pretrain/vocal_models/model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt",
    device="cuda",
    store_dirs="results"
)
separator.separate("input/audio.wav")

# 去混响
separator = MSSeparator(
    model_type="mel_band_roformer",
    config_path="configs/config_vocals_bs_roformer.yaml",
    model_path="pretrain/single_stem_models/dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt",
    device="cuda",
    store_dirs="results"
)
separator.separate("input/vocals.wav")
```

## 与 RVC 配合使用

MSST 可以替代 RVC 自带的 UVR5，提供更好的分离效果：

```
原始音频 → MSST 人声分离 → MSST 去混响 → RVC 训练/推理
```

```powershell
# 在 Python 中一步完成：
# 1. 提取人声 → 2. 去混响 → 3. 输出干净干声
python -c "
from inference.msst_infer import MSSeparator

# 第1步：提取人声
voc = MSSeparator('mel_band_roformer',
    'configs/config_vocals_bs_roformer.yaml',
    'pretrain/vocal_models/model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt',
    device='cuda', store_dirs='temp_vocals')
voc.separate('input/song.mp3')

# 第2步：去混响
dry = MSSeparator('mel_band_roformer',
    'configs/config_vocals_bs_roformer.yaml',
    'pretrain/single_stem_models/dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt',
    device='cuda', store_dirs='output')
dry.separate('temp_vocals/vocals.wav')
"
```
