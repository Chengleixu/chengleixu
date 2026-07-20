---
name: msst-audio-separation
description: MSST-WebUI 音乐源分离 — 人声/伴奏分离、去混响、降噪。支持 CLI 和 Python API
---

# MSST-WebUI 音乐源分离工具

[MSST-WebUI](https://github.com/SUC-DriverOld/MSST-WebUI) (1.2k⭐) 是最先进的音乐源分离工具，比 UVR5 效果更好。

## 位置

```
D:\AI\MSST WebUI\
├── webUI.py                       ← WebUI 入口
├── go-webui.bat                   ← 一键启动 WebUI
├── workenv\python.exe             ← 专用 Python 运行时
├── inference\msst_infer.py        ← MSST 推理 API
├── scripts\
│   ├── msst_cli.py                ← MSST 命令行分离
│   ├── vr_cli.py                  ← VR 模型命令行分离
│   ├── preset_infer_cli.py        ← 预设流程批量处理
│   ├── ensemble_cli.py            ← 多模型集成分离
│   ├── ensemble_audio_cli.py      ← 多音频集成
│   └── some_cli.py                ← 音频转 MIDI
├── pretrain/
│   ├── vocal_models/              ← 人声模型
│   ├── single_stem_models/        ← 降噪/去混响
│   ├── multi_stem_models/         ← 多轨分离
│   └── VR_Models/                 ← UVR 兼容模型
├── configs/                       ← 模型配置 (.yaml)
├── input/                         ← 默认输入目录
└── results/                       ← 默认输出目录
```

## 方式一：CLI 命令行（推荐快速使用）

### 人声分离

```powershell
cd D:\AI\MSST WebUI
.\workenv\python.exe scripts\msst_cli.py ^
  --model_type mel_band_roformer ^
  --config_path "configs/config_vocals_bs_roformer.yaml" ^
  --model_path "pretrain/vocal_models/model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt" ^
  -i "input" -o "results" --output_format wav --device cuda
```

### 去混响

```powershell
.\workenv\python.exe scripts\msst_cli.py ^
  --model_type mel_band_roformer ^
  --config_path "configs/config_vocals_bs_roformer.yaml" ^
  --model_path "pretrain/single_stem_models/dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt" ^
  -i "input" -o "results" --output_format wav --device cuda
```

### 降噪

```powershell
.\workenv\python.exe scripts\msst_cli.py ^
  --model_type mel_band_roformer ^
  --config_path "configs/config_vocals_bs_roformer.yaml" ^
  --model_path "pretrain/single_stem_models/denoise_mel_band_roformer_aufr33_sdr_27.9959.ckpt" ^
  -i "input" -o "results" --output_format wav --device cuda
```

### VR 模型分离

```powershell
.\workenv\python.exe scripts\vr_cli.py ^
  -i "input" -o "results" ^
  -m "pretrain/VR_Models/1_HP-UVR.pth" ^
  --batch_size 4 --window_size 512 --aggression 5
```

### 预设流程（人声分离 → 去混响 → 输出）

```powershell
.\workenv\python.exe scripts\preset_infer_cli.py ^
  -p "preset.json" -i "input" -o "results" -f wav
```

preset.json 示例：
```json
{
    "version": "1.0.0",
    "flow": [
        {"model_type": "vocal_models","model_name": "model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt","input_to_next": "vocals","output_to_storage": []},
        {"model_type": "single_stem_models","model_name": "dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt","input_to_next": "dry","output_to_storage": ["dry"]}
    ]
}
```

## 方式二：Python API

```python
import sys
sys.path.append("D:\\AI\\MSST WebUI")
from inference.msst_infer import MSSeparator

# 人声分离
sep = MSSeparator(
    model_type="mel_band_roformer",
    config_path="D:\\AI\\MSST WebUI\\configs\\config_vocals_bs_roformer.yaml",
    model_path="D:\\AI\\MSST WebUI\\pretrain\\vocal_models\\model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt",
    device="cuda",
    store_dirs="D:\\output"
)
results = sep.process_folder("D:\\input")
sep.del_cache()
```

## 方式三：启动 WebUI

```powershell
cd D:\AI\MSST WebUI
.\go-webui.bat
```

## 与 RVC 配合 — 完整音频预处理管线

```
原始歌曲/视频
    ↓ MSST 人声分离（提取人声）
    ↓ MSST 去混响（去除回声/混响）
    ↓ MSST 降噪（可选）
    ↓ 干净干声 → 用于 RVC 训练或推理
```

```powershell
# 一条命令完成：人声提取 + 去混响
cd D:\AI\MSST WebUI
mkdir temp, final

# 第1步：提取人声
.\workenv\python.exe scripts\msst_cli.py --model_type mel_band_roformer ^
  --config_path configs/config_vocals_bs_roformer.yaml ^
  --model_path pretrain/vocal_models/model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt ^
  -i input -o temp --device cuda

# 第2步：去混响
.\workenv\python.exe scripts\msst_cli.py --model_type mel_band_roformer ^
  --config_path configs/config_vocals_bs_roformer.yaml ^
  --model_path pretrain/single_stem_models/dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt ^
  -i temp -o final --device cuda

# 第3步：用 RVC 推理
cd D:\RVC20240604Nvidia
runtime\python.exe tools\infer_cli.py --model_name nailong ^
  --input_path "D:\AI\MSST WebUI\final\audio.wav" ^
  --opt_path "D:\output_converted.wav" ^
  --index_path logs\added_IVF256_Flat_nprobe_1_tomori_boukaru_v2.index
```

## 可用模型速查

| 用途 | model_type | 模型路径 |
|------|-----------|---------|
| 🎤 人声提取 | `mel_band_roformer` | `pretrain/vocal_models/model_mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt` |
| 🎵 伴奏提取 | `mel_band_roformer` | `pretrain/vocal_models/melband_roformer_inst_v2.ckpt` |
| 🔇 去混响 | `mel_band_roformer` | `pretrain/single_stem_models/dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt` |
| 📉 降噪 | `mel_band_roformer` | `pretrain/single_stem_models/denoise_mel_band_roformer_aufr33_sdr_27.9959.ckpt` |
| 🔄 人声+伴奏 | `bs_roformer` | `pretrain/vocal_models/model_bs_roformer_ep_368_sdr_12.9628.ckpt` |

配置路径统一用：`configs/config_vocals_bs_roformer.yaml`（人声类）或对应的模型配置。
