---
name: video-output-in-chat
description: 视频可以直接用video标签嵌入对话框播放，无需外部链接
metadata:
  type: project
---

## 视频输出方式：对话框直接播放

用户确认 Reasonix 对话框支持 `<video>` 标签，可以直接在回复中嵌入视频播放器。

### 输出格式
```html
<video src="file:///C:/Users/cheng/AppData/Roaming/reasonix/global-workspace/.reasonix/output/{文件名}.mp4" controls width="400"></video>
```

### 流程
1. 生成视频后保存到 `.reasonix\output\` 目录
2. 用 `<video>` 标签嵌入对话框
3. 同时提供在线链接作为备用

### 优势
- 用户直接在对话框点击播放，无需跳转
- 比外部链接更便捷
- 支持播放控制（进度条、音量等）

**Why:** 用户确认 video 标签在对话框中可以正常显示播放器。
**How to apply:** 所有视频输出优先使用 video 标签嵌入对话框，同时在下方提供在线链接作为备用。
