# OpenClaw 技术分享：从 0 到 1 构建 AI 视频创作工作流

> 纯技术视角的 OpenClaw 实战经验与 AI 视频创作技能体系构建

---

## 目录

1. [OpenClaw 简介](#1-openclaw-简介)
2. [快速入门：30 分钟上手指南](#2-快速入门30-分钟上手指南)
3. [实战案例：AI 视频导演技能体系构建](#3-实战案例ai-video 导演技能体系构建)
4. [技能开发最佳实践](#4-技能开发最佳实践)
5. [交互模式与使用心得](#5-交互模式与使用心得)
6. [技术架构深度解析](#6-技术架构深度解析)

---

## 1. OpenClaw 简介

### 1.1 什么是 OpenClaw？

OpenClaw 是一个**AI Agent 技能 orchestration 平台**，核心能力包括：

- **技能系统（Skills）**：模块化的专业知识包，将通用 AI 转化为领域专家
- **工作流编排**：多层技能协同完成复杂任务
- **工具集成**：文件操作、浏览器控制、消息发送、Feishu 集成等
- **会话管理**：支持子代理（subagent）和 ACP 编码会话

### 1.2 核心价值主张

| 传统 AI 使用 | OpenClaw 增强模式 |
|-------------|------------------|
| 每次从零描述需求 | 加载技能后自动具备领域知识 |
| 通用回答，缺乏深度 | 专业化输出，符合行业规范 |
| 单次对话孤立 | 技能沉淀，可复用可分享 |
| 手动整理输出 | 自动化工作流，结构化产出 |

### 1.3 技术特点

- **轻量级**：单个技能文件通常 <10KB
- **声明式**：Markdown 格式，易于编写和维护
- **渐进式加载**：元数据（~100 词）常驻上下文，详细内容按需加载
- **工具无关**：技能可跨平台复用（Discord、Feishu、Telegram 等）

---

## 2. 快速入门：30 分钟上手指南

### 2.1 环境准备（5 分钟）

```bash
# 安装 OpenClaw（需要 Node.js 22+）
npm install -g openclaw

# 初始化工作区
openclaw init my-workspace
cd my-workspace

# 启动 Gateway（后台服务）
openclaw gateway start

# 查看状态
openclaw status
```

### 2.2 第一个技能：Hello World（10 分钟）

创建技能文件 `skills/hello-world/SKILL.md`：

```markdown
---
name: hello-world
description: 测试技能，用于验证 OpenClaw 技能系统正常工作
---

# Hello World Skill

当你看到这个技能被激活，说明技能系统正常工作。

## 能力

- 回复特定问候语
- 展示技能加载状态

## 使用示例

用户：你好
AI：👋 你好！我是 Hello World 技能，我已经成功加载并准备就绪。
```

测试技能：

```bash
# 在对话中触发
openclaw chat "你好"
```

### 2.3 使用现有技能（10 分钟）

#### 从 ClawHub 安装

```bash
# 搜索技能
clawhub search weather

# 安装技能
clawhub install weather-skill

# 使用技能
openclaw chat "北京天气怎么样？"
```

#### 手动安装

```bash
# 克隆技能仓库
git clone https://github.com/your-repo/your-skill.git skills/your-skill

# 技能自动加载（无需重启）
openclaw chat "使用你的技能"
```

### 2.4 验证技能加载（5 分钟）

```bash
# 查看已加载技能
openclaw skills list

# 查看技能详情
openclaw skills show skill-name

# 测试技能触发
openclaw chat "触发技能的专业术语"
```

---

## 3. 实战案例：AI 视频导演技能体系构建

### 3.1 项目背景

**目标**：构建一套完整的 AI 视频创作工作流，从剧本文案到可灵/即梦视频生成的全流程自动化。

**挑战**：
- AI 视频生成需要专业的分镜知识
- 单一技能无法覆盖复杂的多阶段工作流
- 需要确保视觉一致性（角色、场景、风格）

### 3.2 技能架构设计

采用**三层工作流架构**：

```
┌─────────────────────────────────────┐
│ Layer 1: 导演分镜系统                 │
│ - 剧本分析                           │
│ - 情绪节拍拆解                       │
│ - 镜头序列设计                       │
│ - 输出：8 列分镜表格                   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Layer 2: 镜头画面设计与 Prompt 工程    │
│ - 角色/场景视觉资产卡                 │
│ - 首帧参考图 Prompt                  │
│ - 可灵/即梦双平台 Prompt             │
│ - 表演调度方案                       │
│ - 输出：可执行指令包                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ Layer 3: 场景专用镜头序列 Skill 合集   │
│ - 对话场景（正反打系统）              │
│ - 动作场景（打斗/追逐/爆破）         │
│ - 情感场景（情绪弧线匹配）            │
│ - 悬疑场景（紧张感营造）              │
│ - 蒙太奇与转场                       │
└─────────────────────────────────────┘
```

### 3.3 已创建技能清单

#### Layer 1: 导演分镜系统

**技能**：`director-storyboard`

```yaml
目录结构:
  director-storyboard/
  ├── SKILL.md                          # 主技能文档
  ├── references/
  │   ├── director-storyboard-core.md   # 核心执行流程（7 步法）
  │   ├── director-storyboard-advanced.md # 进阶精修模块
  │   ├── camera-language.md            # 镜头语言参考
  │   ├── storyboard-template.md        # 分镜模板
  │   └── ai-video-models.md            # AI 模型适配指南
  ├── scripts/
  │   └── storyboard_generator.py       # Python 示例脚本
  └── assets/
```

**核心能力**：
- 7 步执行流程：剧本解读 → 前置建构 → 角色建立 → 逐镜创作 → 衔接设计 → 节奏控制 → 质量自检
- Key Metrics：500 字剧本≈1.5 分钟，60-120 个镜头
- M2V 记忆机制：保持多镜头角色/场景一致性
- 输出格式：8 列分镜表格（镜头编号/关联剧本/景别/画面描述/情绪&节奏/声音设计/衔接逻辑/运镜提示）

**Git 提交记录**：
```bash
f9e2589 feat: add core and advanced director-storyboard modules
f4becb1 feat: add director-storyboard skill
```

#### Layer 2: 镜头画面设计与 Prompt 工程

**技能**：`camera-prompt-design`

```yaml
目录结构:
  camera-prompt-design/
  ├── SKILL.md                          # 主技能文档
  ├── README.md                         # 用户指南
  ├── references/
  │   ├── director-visual-design-core.md    # 核心版（4Phases）
  │   └── director-visual-design-advanced.md # 进阶版（9Modules）
  ├── scripts/
  └── assets/
```

**核心流程**：
- **Phase 0**: 项目视觉基准（风格锚点、全局 Prompt 后缀）
- **Phase 1**: 角色视觉资产卡（外貌/服装/视觉锚点/参考图 Prompt）
- **Phase 2**: 场景视觉资产卡（空间/物件/光源/色彩）
- **Phase 3**: 逐镜头 Prompt 生成（首帧图 + 可灵 Prompt + 即梦 Prompt + 表演调度）
- **Phase 4**: 镜头分组建议（合并规则、平台推荐）

**关键创新**：
- **消灭抽象情绪词**：将"悲伤"转为"眉头紧锁，眼眶泛红，嘴角向下拉"
- **全中文铁律**：可灵/即梦原生支持中文
- **双平台适配**：同时输出可灵 3.0 和即梦 Seedance 2.0 格式
- **视觉资产卡**：确保角色/场景一致性

**Git 提交记录**：
```bash
1c5960f feat: add camera-prompt-design skill (AI director workflow layer 2)
```

#### Layer 3: 场景专用镜头序列合集

**技能**：`shot-sequence-collection`

```yaml
目录结构:
  shot-sequence-collection/
  ├── SKILL.md                          # 合集主文档
  ├── README.md                         # 使用指南
  ├── references/
  │   ├── Dialogue_Shot_Sequence_Designer.md   # 对话场景
  │   ├── Action_Sequence_Designer.md          # 动作场景
  │   ├── Emotional_Sequence_Designer.md       # 情感场景
  │   ├── Suspense_Thriller_Designer.md        # 悬疑惊悚
  │   └── Montage_Transition_Designer.md       # 蒙太奇与转场
  ├── scripts/
  └── assets/
```

**五大场景技能**：

| Skill | 核心能力 | 参数特点 |
|-------|---------|---------|
| Dialogue | 正反打系统、过肩镜头、反应链、轴线管理 |  avg_shot: 3-5s, 特写 30% |
| Action | 打斗四镜头链、追逐系统、爆破时间轴 | avg_shot: 0.5-1.5s, 特写 40% |
| Emotional | 情绪弧线匹配、留白控制、细腻特写 | avg_shot: 4-8s, 特写 60% |
| Suspense | 紧张感营造、Jump Scare、反转设计 | avg_shot: 1-4s, 特写 45% |
| Montage | 时间压缩、平行叙事、匹配剪辑 | avg_shot: 0.5-3s, 变化大 |

**Git 提交记录**：
```bash
[待提交] feat: add shot-sequence-collection skill
```

### 3.4 技能协作示例

**任务**：将一段情侣争吵剧本转化为可灵视频 Prompt

**工作流**：

```
1. 输入剧本
   └─→ Layer 1 (director-storyboard)
       分析情绪节拍，生成 8 列分镜表
       
2. 分镜表
   └─→ Layer 3 (Emotional_Sequence_Designer)
       匹配"愤怒→悲伤→释然"情绪弧线
       输出镜头序列（含时长、景别建议）
       
3. 镜头序列
   └─→ Layer 2 (camera-prompt-design)
       Phase 0: 确认视觉风格（写实、冷色调）
       Phase 1: 创建角色资产卡（男主/女主）
       Phase 2: 创建场景资产卡（客厅、夜晚）
       Phase 3: 逐镜头生成 Prompt
         - 首帧参考图 Prompt
         - 可灵视频 Prompt
         - 即梦视频 Prompt
         - 表演调度（面部/肢体/视线/微动作）
       Phase 4: 镜头分组建议
       
4. 输出
   └─→ 可直接喂入可灵/即梦的完整指令包
```

---

## 4. 技能开发最佳实践

### 4.1 技能设计原则

#### 4.1.1 渐进式披露（Progressive Disclosure）

```markdown
❌ 错误做法：
在 SKILL.md 中写入所有细节（超过 500 行）

✅ 正确做法：
SKILL.md（<500 行）：核心流程 + 关键时刻
  ↓ 引用
references/core.md：详细执行流程
  ↓ 引用
references/advanced.md：进阶扩展模块
  ↓ 引用
references/camera-language.md：专业知识库
```

**优势**：
- 元数据（name + description）仅~100 词，常驻上下文无负担
- 详细内容仅在技能触发后按需加载
- 支持多层引用，理论无限扩展

#### 4.1.2 单一职责原则

```yaml
# ❌ 错误：一个技能做所有事
name: ai-video-director
description: 从剧本到视频生成的全流程...

# ✅ 正确：职责分离
name: director-storyboard         # Layer 1: 分镜设计
name: camera-prompt-design        # Layer 2: Prompt 工程
name: shot-sequence-collection    # Layer 3: 场景专用模块
```

#### 4.1.3 触发器设计

```yaml
# 好的 description 包含：做什么 + 何时用
description: |
  AI 导演分镜技能，用于视频镜头序列设计、分镜脚本生成、镜头语言规划。
  使用当需要：
  (1) 设计视频分镜脚本，
  (2) 规划镜头序列和转场，
  (3) 生成导演视角的画面描述，
  (4) 将故事/脚本转换为可执行的镜头语言，
  (5) 为 AI 视频生成模型提供结构化分镜输入。

# 包含具体触发场景，AI 更容易判断何时激活技能
```

### 4.2 技能结构模板

```markdown
---
name: skill-name
description: |
  [做什么] + [何时使用] + [输出什么]
  使用当需要：
  (1) 场景 1
  (2) 场景 2
  (3) 场景 3
---

# [Skill 名称]

## 核心定位

- **Role**: [AI 扮演的角色]
- **Core Task**: [核心任务]
- **Output**: [输出格式]

## 核心能力

| 模块 | 功能 | 适用场景 |
|------|------|---------|
| ...  | ...  | ...     |

## 工作流程

```
Step 1 → Step 2 → Step 3 → Output
```

### Step 1: [名称]

[详细说明]

### Step 2: [名称]

[详细说明]

## 输出格式

[表格/代码块/模板]

## 进阶模块

详见 [references/xxx.md](references/xxx.md)

- Module A: ...
- Module B: ...

## 示例

### 输入
> [用户可能的输入]

### 输出
```
[期望的输出格式]
```

## 相关资源

| 文件 | 用途 |
|------|------|
| [xxx.md](references/xxx.md) | 说明 |
```

### 4.3 脚本与资产打包

```yaml
skill-name/
├── SKILL.md              # 必须
├── scripts/              # 可选：可执行脚本
│   ├── example.py        # Python 脚本
│   └── demo.sh           # Bash 脚本
├── references/           # 可选：参考文档
│   ├── core.md
│   └── advanced.md
├── assets/               # 可选：输出用资产
│   ├── template.pptx
│   └── logo.png
└── assets/               # 必须保持目录存在（可为空）
```

**脚本使用建议**：
- 脚本应由 SKILL.md 明确说明何时调用
- 脚本应自包含，依赖最小化
- 脚本输出应易于被 AI 解读

---

## 5. 交互模式与使用心得

### 5.1 典型交互模式

#### 5.1.1 技能创建流程

```
用户：帮我创建一个导演分镜技能
    ↓
AI：理解需求，参考 skill-creator 技能
    ↓
AI：执行以下步骤
    1. mkdir skills/director-storyboard/{scripts,references,assets}
    2. 写入 SKILL.md（包含 YAML frontmatter）
    3. 写入核心参考文档
    4. 创建示例脚本
    5. git add && git commit
    6. git push
    ↓
输出：完整的技能文件夹 + Git 提交
```

#### 5.1.2 技能迭代流程

```
用户：根据公众号文章更新导演分镜技能
    ↓
AI：获取文章内容（web_fetch / 用户粘贴）
    ↓
AI：分析文章结构
    - core.md ← 核心执行流程
    - advanced.md ← 进阶精修模块
    ↓
AI：更新技能文件
    - 新增 references/director-storyboard-core.md
    - 新增 references/director-storyboard-advanced.md
    - 更新 SKILL.md 引用
    ↓
AI：git commit -m "feat: add core and advanced modules"
    ↓
输出：更新后的技能 + Git 提交记录
```

### 5.2 本次项目交互统计

| 指标 | 数值 |
|------|------|
| 创建技能数 | 3 个 |
| 技能文件数 | 15 个 |
| 总代码行数 | ~3000 行 |
| Git 提交数 | 4 次 |
| 使用工具 | exec, write, git |
| 参考文章 | 微信公众号文章 x2 |

### 5.3 关键交互记录

#### 交互 1：创建导演分镜技能

```
用户：按照https://mp.weixin.qq.com/s/...和https://mp.weixin.qq.com/s/...
     把导演分镜 Skill 写成文件夹，并上传到 Git 仓库

AI：
  1. 尝试 web_fetch 获取文章内容（内容被截断）
  2. 尝试 browser 工具（浏览器不可用）
  3. 用户直接粘贴文章内容
  4. AI 分析文章结构：
     - 基础版 → director-storyboard-core.md
     - 进阶版 → director-storyboard-advanced.md
  5. 创建技能文件夹结构
  6. 写入文件：
     - SKILL.md
     - references/camera-language.md
     - references/storyboard-template.md
     - references/ai-video-models.md
     - scripts/storyboard_generator.py
  7. Git 提交并推送

输出：
  ✅ skills/director-storyboard/ 创建完成
  ✅ Git commit: f9e2589
```

#### 交互 2：添加镜头画面设计技能

```
用户：公众号内容（第二篇飞书文档链接 + 三个文件内容）

AI:
  1. 尝试 feishu_doc.read（400 错误）
  2. 用户直接粘贴 README.md + core.md + advanced.md
  3. AI 创建 camera-prompt-design 技能
  4. 写入文件：
     - SKILL.md
     - README.md
     - references/director-visual-design-core.md
     - references/director-visual-design-advanced.md
  5. Git 提交并推送

输出:
  ✅ skills/camera-prompt-design/ 创建完成
  ✅ Git commit: 1c5960f
```

#### 交互 3:创建镜头序列合集

```
用户：分享镜头序列 Skill 合集的 README 和 5 个 Skill 文件

AI:
  1. 创建 shot-sequence-collection 技能
  2. 写入文件:
     - SKILL.md（合集主文档）
     - README.md（使用指南）
     - references/Dialogue_Shot_Sequence_Designer.md
     - references/Action_Sequence_Designer.md
     - references/Emotional_Sequence_Designer.md
     - references/Suspense_Thriller_Designer.md
     - references/Montage_Transition_Designer.md
  3. Git 提交（待完成）

输出:
  ✅ skills/shot-sequence-collection/ 创建完成
```

### 5.4 使用心得

#### ✅ 优势体验

1. **结构化输出**：技能强制 AI 按固定格式输出，质量稳定
2. **知识沉淀**：一次编写，反复使用，不会"失忆"
3. **专业深度**：技能让通用 AI 变成领域专家
4. **Git 版本控制**：每次修改都有记录，可回滚可追溯

#### ⚠️ 注意事项

1. **技能过大**：单个技能>500 行会导致上下文膨胀，应拆分
2. **触发器模糊**：description 不清晰会导致误触发或不触发
3. **过度依赖**：不能替代人类专业判断，AI 输出需审核
4. **工具限制**：browser、feishu_doc 等工具可能不可用，需准备 Plan B

#### 💡 优化建议

1. **技能索引**：创建INDEX.md 记录所有技能和触发词
2. **测试用例**：为每个技能准备 3-5 个测试输入
3. **性能监控**：记录技能加载时间和 token 消耗
4. **用户反馈**：收集实际使用中的问题，持续迭代

---

## 6. 技术架构深度解析

### 6.1 OpenClaw 架构概览

```
┌─────────────────────────────────────────────┐
│           OpenClaw Gateway                  │
│  (后台服务：管理通道、会话、技能加载)          │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│            Channel Plugins                  │
│  (Feishu / Discord / Telegram / WhatsApp)  │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│              Session                        │
│  (当前对话上下文 + 已加载技能元数据)           │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│            Skill System                     │
│  ├── SKILL.md (元数据 + 核心流程)            │
│  ├── references/ (按需加载)                 │
│  ├── scripts/ (可执行)                      │
│  └── assets/ (输出用)                       │
└─────────────────────────────────────────────┘
                     ↕
┌─────────────────────────────────────────────┐
│         AI Model (OpenRouter etc.)         │
│  (接收：系统提示 + 技能内容 + 用户输入)        │
│  (输出：技能增强的专业回答)                  │
└─────────────────────────────────────────────┘
```

### 6.2 技能加载机制

#### 6.2.1 三级加载策略

```
Level 1: 元数据 (常驻上下文)
  - name + description (~100 词)
  - 用于技能触发判断
  - 不占用主要上下文

Level 2: SKILL.md 主体 (<500 行)
  - 核心流程、输出格式、示例
  - 技能触发后加载
  - 占用上下文，需精简

Level 3: References (按需加载)
  - 详细文档、词库、模板
  - AI 自主判断何时读取
  - 理论上无限制
```

#### 6.2.2 技能触发机制

```yaml
触发流程:
  1. 用户输入 → AI 接收
  2. AI 扫描所有技能元数据 (name + description)
  3. 匹配度判断：
     - 关键词匹配
     - 语义相似度
     - 上下文相关性
  4. 触发技能：
     - 加载 SKILL.md 主体
     - AI 按照技能指令执行
  5. 可选：读取 references 文件
```

### 6.3 工具系统集成

| 工具 | 用途 | 本项目使用案例 |
|------|------|---------------|
| `write` | 创建/覆盖文件 | 创建所有 Skill.md 文件 |
| `edit` | 精准编辑文件 | 修复脚本语法错误 |
| `read` | 读取文件 | 读取 skill-creator 模板 |
| `exec` | 执行 shell 命令 | git add/commit/push |
| `web_fetch` | 抓取网页内容 | 尝试获取公众号文章 |
| `browser` | 浏览器自动化 | 备用方案（不可用） |
| `feishu_doc` | 飞书文档读取 | 尝试读取第二篇文章 |
| `git` | 版本控制 | 所有技能提交记录 |

### 6.4 性能与成本优化

#### 6.4.1 Token 优化技巧

```markdown
# ❌ 冗余描述
本技能的主要功能和目的是帮助用户在需要设计视频分镜脚本的时候
能够生成专业的镜头序列设计，这对于 AI 视频创作非常重要...

# ✅ 精简描述
AI 导演分镜技能，用于视频镜头序列设计、分镜脚本生成、镜头语言规划。
使用当需要：(1) 设计分镜脚本，(2) 规划镜头序列...
```

#### 6.4.2 文件组织最佳实践

```yaml
# ✅ 推荐：技能文件 <10KB
director-storyboard/
  ├── SKILL.md (5KB)
  ├── references/core.md (8KB)
  └── references/advanced.md (10KB)

# ❌ 避免：单个文件过大
huge-skill.md (50KB)  # 加载一次占用大量上下文
```

### 6.5 扩展性与未来方向

#### 可能的扩展

1. **技能市场**：ClawHub.com 已初具雏形
2. **技能组合**：多个技能协同工作（如本项目的三层架构）
3. **自动测试**：为技能编写单元测试
4. **性能分析**：监控技能加载时间、token 消耗

#### 技术趋势

1. **多模态技能**：结合图像、音频、视频处理
2. **实时协作**：多人同时与技能交互
3. **技能热更新**：无需重启即可更新技能
4. **跨平台同步**：技能在 Discord/Feishu/Telegram 间同步

---

## 附录

### A. Git 仓库信息

```
仓库：https://github.com/NumbSilver/Skill-by-ClawBot.git
分支：master

提交历史:
1c5960f feat: add camera-prompt-design skill
f9e2589 feat: add core and advanced director-storyboard modules  
f4becb1 feat: add director-storyboard skill
a27bb6d docs: 为前三篇文章添加自媒体钩子
76eaa4d feat: 完成第 07 篇 - Remotion 可编辑广告视频
```

### B. 技能清单

| 技能名 | 文件数 | 行数 | Git Commit |
|-------|-------|------|------------|
| director-storyboard | 5 | ~1200 | f9e2589 |
| camera-prompt-design | 4 | ~1000 | 1c5960f |
| shot-sequence-collection | 6 | ~800 | 待提交 |

### C. 参考资源

- OpenClaw 官方文档：https://docs.openclaw.ai
- ClawHub 技能市场：https://clawhub.com
- 社区 Discord: https://discord.com/invite/clawd
- 本项目仓库：https://github.com/NumbSilver/Skill-by-ClawBot

---

## 总结

本次分享展示了如何使用 OpenClaw 从 0 到 1 构建一个完整的 AI 视频创作工作流。通过三层技能架构（导演分镜 → Prompt 工程 → 场景专用模块），我们实现了从剧本文案到可执行视频生成 Prompt 的全流程自动化。

**核心收获**：
1. **技能系统**：让通用 AI 变成领域专家的关键
2. **渐进式披露**：管理上下文复杂度的最佳实践
3. **工作流编排**：多层技能协同完成复杂任务
4. **Git 版本控制**：技能迭代的可靠保障

**下一步**：
- 继续完善 shot-sequence-collection 技能
- 添加更多场景专用模块（独白、奇幻、日常）
- 实际测试整个工作流（剧本 → 视频生成）
- 分享技能到 ClawHub 社区

---

*最后更新时间：2026-03-05*  
*作者：OpenClaw 用户*  
*许可证：MIT*
