---
name: generative-media-skills-patterns
description: 从 Generative-Media-Skills (3.9k⭐) 学到的视频生成工作流设计模式
metadata:
  type: reference
---

**来源：** [SamurAIGPT/Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) (3.9k⭐)

**核心设计模式：**
- **Recipe Pack 模式**：每个视频/图像生成任务 = 一个独立的 recipe（SKILL.md），声明 inputs + Steps
- **Core/Library 分离**：Core 是底层 API 封装，Library 是领域专家技能
- **MCP Server 模式**：通过 MCP 暴露 19 个结构化工具给任何 AI agent
- **Agentic Pipeline**：JSON 结构化输出 + `--jq` 过滤 + 语义退出码，支持管道链式调用

**关键 Recipe 示例（对你最有用的）：**
- `character-story-video` — 多部分动画故事，保持角色一致性
- `cinema-director` — 导演级电影提示词生成
- `seedance-2` — 图生视频 + 视频扩展

**如何应用：**
- 已将 Recipe Pack 模式适配到你的 [character-video-pipeline](skill:character-video-pipeline) 自定义 skill
- Core/Library 分离可用于组织你的视频生成脚本
- 阿里云百炼的 MCP 模式类似，可参考其结构化工具设计

**Why:** 你的项目大量依赖 AI 视频生成（见 [video-generation-lessons](video-generation-lessons.md)），这个项目的 41 个工作流提供了经过验证的设计模式
