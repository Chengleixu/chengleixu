---
name: karpathy-coding-discipline
description: Andrej Karpathy AI 编码规范：先思考、极简、手术式修改、目标驱动
metadata:
  type: feedback
---

**来源：** [meisijiya/Efficient-Reasonix](https://github.com/meisijiya/Efficient-Reasonix) — 整合自 Andréj Karpathy 的 AI 编码规范

**四条核心规则：**
1. **先思考再动手** — 不确定就问，展示 trade-off，不隐藏困惑
2. **极简优先** — 最少代码解决问题，不添加未要求的功能/抽象/灵活性
3. **手术式修改** — 只碰必须碰的，只清理自己造成的混乱，每一行改动可溯源到需求
4. **目标驱动执行** — 定义可验证的成功标准，循环直到验证通过

**Why:** 这四条规则能显著减少 diff 中不必要的改动和因过度设计导致的推倒重来
