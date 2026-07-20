---
name: reasonix-desktop-pet
description: 生成 Reasonix Dropout Bear 桌面宠物（Electron + Canvas 精灵动画）
---

# Reasonix 桌宠生成器

生成一个 Dropout Bear 风格的桌面宠物（Electron 应用），具备完整的精灵图动画、音乐播放、文件拖放等功能。

## 项目结构

```
reasonix-pet/
├── package.json          # Electron 依赖
├── main.js               # 主进程（窗口管理/托盘/IPC/音频扫描/文件读取）
├── preload.js            # 安全桥接层（暴露 IPC 方法给渲染进程）
├── start-hidden.vbs      # 静默启动脚本（无黑框）
├── start.bat             # 调试启动脚本（有控制台）
└── src/
    ├── index.html        # 主页面
    ├── style.css         # 样式（UI/布局/动画/音符特效）
    ├── renderer.js       # 核心渲染/交互逻辑
    └── assets/
        ├── covers/       # 专辑封面（本地 JPG）
        ├── eating/       # 吃饼干单帧
        ├── failed/       # 失败动画 8 帧
        ├── idle/         # 空闲动画 6 帧
        ├── jumping/      # 跳跃动画 5 帧
        ├── review/       # 审视动画 6 帧
        ├── running/      # 跑步动画 6 帧
        ├── running-left/ # 向左跑 8 帧
        ├── running-right/# 向右跑 8 帧
        ├── waiting/      # 等待动画 6 帧
        └── waving/       # 挥手动画 4 帧
```

## 创建步骤

1. **初始化项目**
   - 创建文件夹 `reasonix-pet/` + `src/` + `src/assets/`
   - `package.json` 配置 `electron` 依赖

2. **主进程 (main.js)**
   - 无边框透明窗口 280×360，始终置顶
   - 系统托盘（右键菜单含开机自启开关）
   - IPC handlers：聊天/拖拽/文件读取/音频列表/剪贴板

3. **动画系统 (renderer.js)**
   - `frameCache` 预加载所有 PNG 帧，绿幕抠图
   - `requestAnimationFrame` 帧循环，60fps
   - 8 种动画状态 + 1 个单帧 eating 状态
   - `drawHeadphones` / `drawSnapSpark` Canvas 叠加特效

4. **精灵图要求**
   - 每帧 192×208px，绿幕 #00FF00
   - 状态编码到目录名，帧编码到文件名 `00.png` `01.png` ...
   - 加载时自动去除绿幕

## 核心功能

| 功能 | 实现 |
|---|---|
| 拖拽 | `screenX` 绝对坐标定位，3px 阈值 |
| 聊天气泡 | 头顶浮出，自动消失 |
| 音乐播放器 | 🎧 耳机模式，💿 专辑/FM 双模式 |
| 文件拖放 | 拖文件到小熊 → 读取 + 分析 + 剪贴板 |
| 复合动作 | 10 组多状态序列（打哈欠/打招呼/蹦跳） |
| 音符特效 | Canvas 音符浮动 + 光环 |
| 耳机绘制 | Canvas 4 层结构 + 网孔 + 头梁 |
| 缩放 | CSS transform 50%~200% |
| 开机自启 | `app.setLoginItemSettings` |
| 单例锁 | `app.requestSingleInstanceLock` |

## 关键技术点

- **绿幕去背景**: Chroma key 阈值 55，RGB 距离 < 55 则透明化
- **动画状态切换**: `setState()` 重置帧索引，`animate()` 按 speed 推进
- **UI 位置自适应**: `applyZoom()` 计算小熊视觉底部，动态调整操作栏位置
- **专辑曲目排序**: `ALBUM_TRACKS` 硬编码 + `extractTitle` 智能匹配文件名
- **双模式播放**: 专辑顺序 / FM 随机全库洗牌
