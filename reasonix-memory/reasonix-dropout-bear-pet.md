---
name: reasonix-dropout-bear-pet
description: Reasonix Dropout Bear 桌宠项目位置和架构
metadata:
  type: project
---

# Reasonix Dropout Bear 桌宠

**项目位置**: `C:\Users\cheng\AppData\Roaming\reasonix\global-workspace\reasonix-pet\`
**启动方式**: 双击桌面 `Reasonix桌宠` 快捷方式，或 `npx electron .`

## 核心文件

| 文件 | 作用 |
|---|---|
| `main.js` | Electron 主进程：窗口管理、IPC、托盘、开机自启、音频扫描、单例锁 |
| `preload.js` | 安全桥接：暴露 chat/moveWindow/readFiles/listMusicLibrary/clipboardWrite 等方法 |
| `src/index.html` | UI 结构：canvas、操作栏、设置面板、聊天气泡 |
| `src/style.css` | 完整样式：布局、毛玻璃 UI、音乐音符动画、耳机样式、专辑封面 |
| `src/renderer.js` | 核心 (~1600 行)：精灵动画、耳机绘制、音乐播放、文件处理、复合动作 |

## 精灵图资源

`src/assets/` 下 11 个目录：idle/waiting/waving/jumping/running/running-left/running-right/review/failed/eating + covers（专辑封面）

每帧 192×208px，绿幕 #00FF00，加载时 chroma key 阈值 55 自动去背景。

## 关键架构

- **显示**: Electron 无边框透明窗口 280×360，canvas 200×240，CSS transform 缩放
- **动画**: 每帧用 `requestAnimationFrame`，8 种状态 + 帧循环
- **交互**: 拖拽（screenX 绝对定位）、10 组复合动作、音乐播放器
- **音乐**: 双模式（💿 专辑按 tracklist + 📻 FM 随机），监听 🎧 单击/双击
- **桌面集成**: 系统托盘、开机自启、单实例锁、VBS 静默启动

## 用户偏好

- 默认缩放 180%
- 默认耳机银色
- 专辑封面本地存储
- 状态栏 10s 自动隐藏，鼠标靠近底部显示
- 设置面板点击外部关闭
