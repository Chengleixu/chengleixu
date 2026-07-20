#!/usr/bin/env python3
"""Vision API 调用脚本 — 封装图片编码、API 请求、结果解析"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error

# ---- 配置（可通过环境变量覆盖） ----
API_URL = os.environ.get(
    "VISION_API_URL",
    "<your-api-endpoint>/v1/chat/completions",
)
API_KEY = os.environ.get("VISION_API_KEY", "<your-api-key>")
MODEL = os.environ.get("VISION_MODEL", "<首选模型名称>")
FALLBACK_MODEL = os.environ.get("VISION_FALLBACK", "<备选模型名称>")
FALLBACK_API_URL = os.environ.get("VISION_FALLBACK_API_URL", "")
FALLBACK_API_KEY = os.environ.get("VISION_FALLBACK_API_KEY", "")
MAX_TOKENS = int(os.environ.get("VISION_MAX_TOKENS", "3000"))
TEMPERATURE = float(os.environ.get("VISION_TEMPERATURE", "0.3"))
TIMEOUT = int(os.environ.get("VISION_TIMEOUT", "120"))

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
MAX_FILE_SIZE_MB = 10


def encode_image(path: str) -> str:
    """读取图片文件并返回 base64 编码"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"图片不存在: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的图片格式: {ext}，支持: {ALLOWED_EXTENSIONS}")
    size_mb = os.path.getsize(path) / 1048576
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"图片过大: {size_mb:.1f}MB，超过 {MAX_FILE_SIZE_MB}MB 限制")
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_api(image_source: str, question: str) -> dict:
    """调用多模态 API，返回解析后的结果"""
    if image_source.startswith(("http://", "https://")):
        image_url = image_source
    else:
        try:
            b64 = encode_image(image_source)
            ext = os.path.splitext(image_source)[1][1:] or "jpeg"
            image_url = f"data:image/{ext};base64,{b64}"
        except (FileNotFoundError, ValueError) as e:
            return {"success": False, "error": str(e)}

    models = [m.strip() for m in [MODEL, FALLBACK_MODEL] if m.strip()]

    for i, model in enumerate(models):
        url = FALLBACK_API_URL if i > 0 and FALLBACK_API_URL else API_URL
        key = FALLBACK_API_KEY if i > 0 and FALLBACK_API_KEY else API_KEY
        payload = json.dumps({
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question or "请详细描述这张图片中的内容"},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return {
                    "success": True,
                    "model": model,
                    "description": result["choices"][0]["message"]["content"],
                    "usage": result.get("usage", {}),
                }
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            if e.code == 401:
                return {"success": False, "error": "API Key 无效，请检查密钥"}
            if e.code == 404 and "endpoints" in body:
                continue
            if e.code in (408, 504) or "Timeout" in body:
                return {"success": False, "error": "请求超时，图片可能过大"}
            return {"success": False, "error": f"HTTP {e.code}: {body[:200]}"}
        except urllib.error.URLError as e:
            return {"success": False, "error": f"网络错误: {e.reason}"}
        except json.JSONDecodeError:
            return {"success": False, "error": "API 返回格式异常"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    return {"success": False, "error": "所有模型均不可用"}


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python vision_api.py <图片路径或URL> [问题]")
        sys.exit(1)

    image_source = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else ""

    result = call_api(image_source, question)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
