---
name: video-output-manager
description: 视频生成后自动保存到本地固定目录+上传在线链接+提供file://本地路径，方便直接获取MP4文件
---

# 视频输出管理 Skill

生成视频后，自动执行以下流程提供文件获取方式。

## 输出路径规范

所有生成的视频统一保存到以下目录：
```
C:\Users\cheng\AppData\Roaming\reasonix\global-workspace\.reasonix\output\
```

文件名格式：`{项目名}_{日期}_{序号}.mp4`

## 用户获取方式（优先级从高到低）

### 1. 本地文件路径（最快）
直接告知用户本地路径，用户可在文件管理器中直接打开：
```
file://C:\Users\cheng\AppData\Roaming\reasonix\global-workspace\.reasonix\output\xxx.mp4
```

### 2. 在线链接（备用）
同时上传到临时托管服务，提供可直接播放的链接。

### 3. 确认用户能打开本地文件
询问用户是否能直接访问该路径，如果不能则只给在线链接。

## 执行步骤

```powershell
# 1. 确保输出目录存在
mkdir -p ".reasonix/output"

# 2. 生成/下载视频后复制到输出目录
Copy-Item "源文件.mp4" ".reasonix/output/{文件名}.mp4"

# 3. 上传在线备份
npx -y agnes-ai-cli@^0.1.0 media url ".reasonix/output/{文件名}.mp4" --json

# 4. 同时告知用户：
#    - 本地路径（可直接双击播放）
#    - 在线链接（浏览器打开）
```

## 配合主 skill 使用
此 skill 作为 `alibaba-video-generator` 的补充，在最后一步调用。
