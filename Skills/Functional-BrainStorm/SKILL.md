---
name: Functional-BrainStorm
description: 当用户要求外部调研时，或主动召唤时触发；用于外部调研、实现思路发散、方案对比、风险挖掘与落地收敛。
skill_mode: guide_only
metadata:
  doc_structure:
    doc_id: functional_brainstorm.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Functional-BrainStorm skill
---

# Functional-BrainStorm

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能用于外部调研、实现思路发散、方案对比、风险与边界挖掘，以及最终落地路径收敛。
- 当任务涉及前端美术设计、布局脑洞、动画语言或产品氛围探索时，也可以直接用它来扩展视觉方向。
- 本技能专注于思考与调研本身；你可以直接开始看资料、归纳模式、提出建议，不需要依赖本地工具。
- 本技能鼓励你替用户多想一步：先看已知方向，再主动补充更多角度，帮助用户看到更完整的可能性空间。

### 2. 技能约束
- 优先从高信噪比的一手源开始：
  - 官方文档
  - 官方博客 / 工程博客
  - GitHub 仓库、issue、discussion
  - 产品帮助中心、定价页、发布日志
  - 架构中心、设计系统、公开分享
- 输出时把内容整理成三层：
  - 证据
  - 推断
  - 建议
- 在总结“别人怎么做”时，顺手补上：
  - 为什么这样做
  - 适用前提
  - 成本、边界与迁移难点
- 如果信息新鲜度会影响结论，先补最新资料，再继续收敛建议。
- 调研的目标是提炼可迁移模式，把外部经验转成当前任务可执行的思路。

### 3. 顶层常驻合同
- 优先输出“模式、权衡、适用条件、落地建议”，让用户快速看到真正有用的结论。
- 当外部案例彼此冲突时，主动指出冲突点，这会让建议更稳。
- 当结论依赖假设时，把假设讲清楚，这样后续可以继续验证。
- 如果用户最终要落到当前 repo、当前产品或当前技能体系，结尾顺手给出可接续的下一步建议。

## 2. 技能正文
### 1. 功能入口
- [大厂经验调研]
  - 作用：调研成熟产品、平台或大厂团队在相近问题上的真实做法。
  - 可以先看这些地方：
    - `https://aws.amazon.com/architecture/`
    - `https://cloud.google.com/architecture`
    - `https://learn.microsoft.com/azure/architecture/`
    - `https://netflixtechblog.com/`
    - `https://www.uber.com/blog/engineering/`
    - `https://github.com/`
  - 然后继续顺着官方链接、发布日志、开源仓库、竞品页面往外扩，尽量把共同模式和关键差异一起找出来。
  - 输出：已观察模式、共同做法、差异点、适用前提、可借鉴部分。

- [实现思路发散]
  - 作用：围绕一个问题发散多种可能实现路线，而不是过早收缩到单解。
  - 可以先看这些地方：
    - `https://github.com/`
    - `https://stackoverflow.com/`
    - `https://news.ycombinator.com/`
    - `https://www.reddit.com/`
    - `https://www.youtube.com/`
    - 对应技术栈的官方文档与 example 仓库
  - 欢迎从不同实现风格出发继续扩展，比如工程化、平台化、低成本 MVP、长期演进、易维护性这些角度都可以主动补进去。
  - 输出：至少 3 条候选路线，每条都有优点、缺点、依赖前提与失败风险。

- [前端美术设计发散]
  - 作用：围绕前端视觉风格、奇特布局、动画节奏、交互氛围和组件表现力发散灵感，特别适合 Vue 与其生态。
  - 可以先看这些地方：
    - `https://www.awwwards.com/`
    - `https://www.behance.net/`
    - `https://dribbble.com/`
    - `https://www.land-book.com/`
    - `https://godly.website/`
    - `https://mobbin.com/`
    - `https://tympanus.net/codrops/`
    - `https://gsap.com/showcase/`
    - `https://vueuse.org/`
    - `https://motion.vueuse.org/`
    - `https://www.naiveui.com/`
    - `https://www.vuetifyjs.com/`
    - `https://primevue.org/`
    - `https://ui.nuxt.com/`
    - `https://www.shadcn-vue.com/`
  - 鼓励你主动从更多角度继续延伸，比如字体、配色、留白、动效节奏、滚动叙事、装饰图形、卡片语言、信息密度、移动端触感这些方向都值得多看几轮。
  - 这里尤其适合替用户多想一些反常规方向：大胆一点、奇怪一点、风格化一点，再回头判断哪些能落到 Vue 生态里。
  - 输出：可借鉴风格、布局模式、动画语言、适配 Vue 生态的落地思路、需要规避的前端实现风险。

- [Python 奇技淫巧发散]
  - 作用：寻找那种几行就解决漂亮问题、思维跳跃感强、写法精巧的 Python 方案与表达方式。
  - 可以先看这些地方：
    - `https://wiki.python.org/moin/Powerful%20Python%20One-Liners`
    - `https://codegolf.stackexchange.com/`
    - `https://www.pythonmorsels.com/`
    - `https://holypython.com/100-python-tips-tricks/`
    - `https://treyhunner.com/`
    - `https://realpython.com/`
    - `https://www.reddit.com/r/Python/`
    - `https://www.reddit.com/r/codegolf/`
    - `https://stackoverflow.com/questions/tagged/python`
  - 这里很适合主动从更多方向继续外扩，比如：
    - one-liner
    - comprehension 技巧
    - itertools / functools / operator 的巧用
    - 数据结构小技巧
    - 递归 / 生成器 / 闭包的精巧写法
    - 可读性与炫技之间的平衡
  - 也欢迎你替用户多想一点：不仅找“牛逼写法”，也顺手判断哪些值得借鉴，哪些更适合作为灵感而不适合直接落地。
  - 输出：值得借鉴的写法模式、适用场景、潜在坑点、可迁移到当前任务的表达方式。

- [邪修玩法发散]
  - 作用：寻找那些不走寻常路、把现有组件、机制、提示词、工作流或工具换个思路用之后产生奇效的玩法。
  - 可以先看这些地方：
    - `https://news.ycombinator.com/`
    - `https://www.reddit.com/`
    - `https://github.com/`
    - `https://www.producthunt.com/`
    - `https://www.indiehackers.com/`
    - `https://www.youtube.com/`
    - `https://twitter.com/`
    - `https://x.com/`
    - 各类 issue / discussion / showcase / experimental docs 页面
  - 这里很适合主动去找这些模式：
    - 组件错位复用
    - 工作流重新编排
    - 提示词打包后插入不同位置
    - 原本面向 A 的能力被挪到 B 的场景里
    - 把多个普通能力拼出一个意外高效的新入口
  - 这类方向特别值得替用户多想几步：不仅看“原作者打算怎么用”，也看“还能被怎么挪用”“在哪些位置插进去会产生奇效”“有没有比标准解更灵活的玩法”。
  - 输出：可借鉴的邪修玩法、适用场景、为什么有效、可迁移方式、潜在副作用与边界。

- [方案对比收敛]
  - 作用：对多个候选路线做取舍，收敛出当前阶段最合适的方案。
  - 可以优先结合这些输入来收敛：
    - 官方文档里的限制与最佳实践
    - GitHub issue / discussion 里的真实坑点
    - 产品帮助中心、发布日志、定价页里的产品边界
    - 当前项目的时间、复杂度、维护成本约束
  - 收敛时鼓励你替用户多看两步：不仅比较“能不能做”，也比较“后面会不会难养”。
  - 输出：推荐方案、放弃方案、放弃原因、最终选择依据。

- [风险与边界挖掘]
  - 作用：提前暴露实现中的隐性风险、边界条件、迁移成本与维护成本。
  - 可以先看这些地方：
    - GitHub issues / discussions
    - 官方 limitations / known issues 页面
    - 发布日志与 breaking changes
    - 故障复盘、迁移指南、兼容性说明
    - 社区问答与实际踩坑分享
  - 这里很适合主动换视角：从用户、维护者、部署者、未来扩展者的角度各看一遍，通常会得到更完整的风险图。
  - 输出：关键风险列表、触发条件、缓解思路、必须先确认的问题。

- [落地路径建议]
  - 作用：把前面的调研与脑暴结果收敛成一条当前可执行的落地路径。
  - 可以优先参考这些地方来组织落地顺序：
    - 官方 quickstart / getting started
    - 官方 migration guide
    - 示例仓库的最小可运行骨架
    - 产品帮助中心的接入顺序
    - 已有项目约束与现状
  - 这里鼓励你同时给出：
    - 最小起步方案
    - 第一轮验证点
    - 后续扩展路线
  - 输出：建议顺序、最小起步方案、验证点、后续扩展方向。

### 2. 输出要求
- 默认输出顺序：
  - 问题重述
  - 外部证据
  - 模式归纳
  - 方案建议
  - 风险与下一步
- 当用户只要求发散时，可以减少收敛强度；同时继续保留每条候选方向的适用前提与边界。
- 当用户要求最终建议时，明确推荐项与不推荐项，会让结果更好用。
- 在已经提供的站点之外，继续主动探索更多同类来源是被鼓励的；越能从不同角度替用户补充思考，这个技能就发挥得越完整。

## 3. 目录结构图
```text
Functional-BrainStorm/
├── SKILL.md
└── agents/
    └── openai.yaml
```
