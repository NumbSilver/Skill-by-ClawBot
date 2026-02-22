---
name: remotion-video
description: 用于创建 Remotion 视频模板的 Skill。当需要创建新的视频模板、匹配动画组件、实现脚本匹配和布局设计时使用。自动从 AnimationComponent 中选择合适的动画组件，如果不存在则仿照现有结构生成新组件。创建的模板遵循 modules/motion-editor/src/remotion/VideoTemplate 的风格和布局规范。支持智能组件匹配、布局自动化和最佳实践。
---

# Remotion Video Template Creator

## 概述

这个 Skill 帮助你创建符合项目规范的 Remotion 视频模板。它能够：
- 自动匹配和选择 AnimationComponent 中的动画组件
- 实现脚本与动画的智能匹配
- 自动生成符合项目风格的布局
- 在 AnimationComponent 中不存在所需动画时，仿照现有结构生成新组件
- 在 `modules/motion-editor/src/remotion/VideoTemplate` 下创建新的模板

---

## Quick Start

```bash
# 使用 Python 脚本生成模板骨架
python scripts/generate_template.py TemplateName --path ./VideoTemplate
```

---

## 何时使用

在以下场景使用此 Skill：
- 需要创建新的视频模板
- 需要为特定脚本匹配动画效果
- 需要生成符合项目规范的视频布局
- 需要创建新的动画组件（当现有组件不满足需求时）

---

## 工作流程

### 1. 理解需求

首先明确：
- 视频模板的用途和场景
- 需要展示的内容类型（文本、视频、图片等）
- 期望的动画效果和风格
- 脚本的时间分段信息（segmentationArray 和 segmentationArrayKeyWords）

### 2. 动画组件匹配

**优先使用现有组件**：
1. 查看 `references/animation_components.md` 了解所有可用组件
2. **参考动画组件库**：所有可用的动画组件定义在 `modules/motion-editor/src/remotion/animation_components.json` 中，包含完整的组件信息、tags、intent 和 slots 配置。在选择动画组件时，必须参考此文件进行匹配。
3. 根据需求匹配最合适的组件

**组件选择决策树：**
```
需要什么类型的内容？
├── 文本展示
│   ├── 单个文本 → Anim_Text_01
│   └── 序列文本 → Anim_SerialText_01
├── 视频展示
│   ├── 多视频网格 → Anim_VideoGrid_01
│   ├── 旋转轮播 → Anim_VideoTransform_01
│   ├── 随机切片 → Anim_RandomCutVideo_01
│   └── 场景切换 → Anim_RandomSwitchSceneVideo_01
├── 装饰效果
│   ├── 烟花 → Anim_FireworkParticles_01
│   ├── 遮罩 → Anim_ExpandingCircleMask_01
│   ├── 边框 → Anim_DoubleBorder_01
│   └── 信息展示 → Anim_AgencyInfo_01
└── 容器包装 → Anim_Container_01
```

**创建新组件（如需要）**：
1. 参考 `references/component_structure.md` 了解组件结构
2. 仿照 `modules/motion-editor/src/remotion/AnimateComponent` 中类似组件的结构
3. 在 `animation_components.json` 中注册新组件

### 3. 创建模板结构

每个模板应包含：

```typescript
// 1. Schema 定义（使用 zod）
export const TemplateNameSchema = z.object({
  src: z.string(),
  composition: z.string().optional(),
  endSrc: z.string(),
  segmentationArray: z.array(z.number()),
  segmentationArrayKeyWords: z.array(z.array(z.string())),
  _seed: z.number().optional(),
});

// 2. 元数据计算函数
export const calculateTemplateNameMetadata: CalculateMetadataFunction<
  z.infer<typeof TemplateNameSchema>
> = async ({ props }) => {
  const fps = 30;
  try {
    const metadata = await getVideoMetadata(props.src);
    return {
      fps,
      durationInFrames: Math.floor(metadata.durationInSeconds * fps) + 50,
    };
  } catch (error) {
    console.error('获取视频元数据失败:', error);
    return {
      fps,
      durationInFrames: 1630, // 默认值
    };
  }
};

// 3. 主组件
export const TemplateName: React.FC<z.infer<typeof TemplateNameSchema>> = ({
  src,
  endSrc,
  segmentationArray,
  segmentationArrayKeyWords,
}) => {
  const { durationInFrames } = useVideoConfig();
  const scriptCount = segmentationArrayKeyWords.length;
  
  // 实现模板逻辑
};
```

### 4. 布局和样式规范

参考现有模板（如 `BossSuccessVideo`, `AIVideo`）的布局模式：
- 使用 `AbsoluteFill` 作为根容器
- 使用 `Container` 包装主要动画
- 使用 `Sequence` 控制时间轴
- 使用项目字体（`TikTokSansText`）

---

## 🔴 关键规则（必须遵守）

### 1. Logo 注入规则（强制）

**每个模板必须包含 Logo**：
```typescript
import { staticPlatformCdn } from '@/Utils/cdn';

// 在 AbsoluteFill 根容器内、Series 之前添加
<img
  src={staticPlatformCdn('images/bailogo.png')}
  style={{
    position: 'absolute',
    zIndex: '900',
    width: '70%',
    top: '2%',
    left: '15%',
  }}
/>
```

**规则要点：**
- Logo 必须使用 `staticPlatformCdn('images/bailogo.png')` 路径
- zIndex 设置为 900，确保在所有内容之上
- 位置固定在顶部（top: '2%', left: '15%'）
- 宽度为 70%

### 2. 颜色系统（禁止硬编码）

**所有颜色必须从 `@/Utils/Color` 导入**：
```typescript
import { primaryColors, secondaryColors, neutralColors, rgbaColor } from '@/Utils/Color';

// ✅ 正确用法
color: primaryColors[0]
backgroundColor: rgbaColor(primaryColors[1], 0.7)
textColor: neutralColors[5]  // 白色

// ❌ 禁止用法
color: '#000'
backgroundColor: 'white'
color: 'rgb(255, 0, 0)'
```

**可用颜色：**
- `primaryColors` - 主色数组
- `secondaryColors` - 次色数组
- `neutralColors` - 中性色数组（黑色、白色等）
- `rgbaColor(color, opacity)` - 颜色透明度工具函数
- `getColorPalette()` - 获取完整调色板

### 3. 脚本布局规则

**重要限制**：如果脚本数量超过5个，这些脚本**不能**出现在画面中部（position: [50, 50]）

```typescript
const scriptCount = segmentationArrayKeyWords.length;

// 根据脚本数量选择位置
const textPosition = scriptCount > 5 ? [50, 25] : [50, 50];
```

**推荐位置：**
- 顶部区域：`position: [50, 20-30]`
- 中部区域：`position: [50, 50]`（仅当脚本数量 ≤ 5 时使用）
- 底部区域：`position: [50, 70-80]`
- 左侧区域：`position: [25-35, 50]`
- 右侧区域：`position: [65-75, 50]`

### 4. CTA 时间位置

**CTA 必须在视频结尾的后3秒内显示**：
```typescript
// CTA 从 durationInFrames - 90 帧开始（fps=30 时，90帧=3秒）
const ctaStartFrame = durationInFrames - 90;
```

### 5. 动画组件参考

**选择动画组件时必须参考**：`modules/motion-editor/src/remotion/animation_components.json`

该文件包含所有可用组件的完整信息：
- tags（标签）
- intent（用途说明）
- slots（插槽配置）
- structure_type（结构类型）

---

## 动画模式示例

### 文本动画
```typescript
<AnimationText
  baseProps={{
    content: segmentationArrayKeyWords[0]?.[0],
    position: scriptCount > 5 ? [50, 25] : [50, 50],
  }}
  effects={[{
    type: TextEffectType.OUTLINE,
    config: { 
      outlineColor: neutralColors[5],
      thickness: 5 
    },
  }]}
  animations={[{
    type: TextAnimationType.POP,
    config: { durationInFrames: 30, trigger: 'onEnter' },
  }]}
/>
```

### 容器动画
```typescript
<Container
  animations={[{
    type: ContainerAnimationType.ZOOM_IN_BLUR,
    config: {
      animationDelay: durationInFrames,
      animationDuration: 45,
    },
  }]}
>
  {/* 子内容 */}
</Container>
```

### 分段脚本展示
```typescript
{segmentationArray.map((startTime, index) => (
  <Sequence
    key={index}
    from={startTime}
    durationInFrames={segmentationArray[index + 1] - startTime || 60}
  >
    <AnimationText
      baseProps={{
        content: segmentationArrayKeyWords[index]?.[0],
        position: scriptCount > 5 ? [50, 25] : [50, 50],
      }}
    />
  </Sequence>
))}
```

---

## 组件选择指南

### 文本相关
| 组件 | 用途 |
|------|------|
| `Anim_Text_01` | 基础文本动画，支持多种效果和动画类型 |
| `Anim_SerialText_01` | 序列文本，按时间显示多个文本 |

### 视频相关
| 组件 | 用途 |
|------|------|
| `Anim_VideoGrid_01` | 视频网格布局（4个或6个视频） |
| `Anim_VideoTransform_01` | 视频旋转轮播 |
| `Anim_RandomCutVideo_01` | 随机切片段 |
| `Anim_RandomSwitchSceneVideo_01` | 场景切换转场 |
| `Anim_RandomCTAEndVideo_01` | 随机CTA结束视频 |
| `Anim_LoopableOffthreadVideo_01` | 可循环的离线视频 |

### 装饰相关
| 组件 | 用途 |
|------|------|
| `Anim_FireworkParticles_01` | 烟花粒子效果 |
| `Anim_ExpandingCircleMask_01` | 圆形扩展遮罩 |
| `Anim_DoubleBorder_01` | 双重边框动画 |
| `Anim_ExpandingBox_01` | 扩展盒子动画 |
| `Anim_AgencyInfo_01` | 机构信息展示 |
| `Anim_Lottie_01` | Lottie动画组件 |
| `Anim_ImageSeries_01` | 图片序列组件 |

### 容器相关
| 组件 | 用途 |
|------|------|
| `Anim_Container_01` | 容器组件，提供动画包装 |

---

## 模板创建示例

### 完整模板示例

```typescript
import {
  AbsoluteFill,
  OffthreadVideo,
  Series,
  Sequence,
  useVideoConfig,
} from 'remotion';
import { z } from 'zod';
import { getVideoMetadata } from '@remotion/media-utils';
import { primaryColors, neutralColors, rgbaColor } from '@/Utils/Color';
import { staticPlatformCdn } from '@/Utils/cdn';
import { TikTokSansText } from '@/Utils/load-font';
import AnimationText from '@/remotion/AnimateComponent/Text';
import Container from '@/remotion/AnimateComponent/Container';
import {
  TextAnimationType,
  TextEffectType,
} from '@/remotion/AnimateComponent/Text/constants';
import {
  ContainerAnimationType,
} from '@/remotion/AnimateComponent/Container/constants';

// Schema 定义
export const DemoTemplateSchema = z.object({
  src: z.string(),
  composition: z.string().optional(),
  endSrc: z.string(),
  segmentationArray: z.array(z.number()),
  segmentationArrayKeyWords: z.array(z.array(z.string())),
  _seed: z.number().optional(),
});

// 元数据计算
export const calculateDemoTemplateMetadata = async ({ props }) => {
  const fps = 30;
  try {
    const metadata = await getVideoMetadata(props.src);
    return {
      fps,
      durationInFrames: Math.floor(metadata.durationInSeconds * fps) + 50,
    };
  } catch (error) {
    console.error('获取视频元数据失败:', error);
    return { fps, durationInFrames: 1630 };
  }
};

// 主组件
export const DemoTemplate = ({
  src,
  segmentationArray,
  segmentationArrayKeyWords,
}) => {
  const { durationInFrames } = useVideoConfig();
  const scriptCount = segmentationArrayKeyWords.length;
  const textPosition = scriptCount > 5 ? [50, 25] : [50, 50];

  return (
    <AbsoluteFill style={{ backgroundColor: neutralColors[0] }}>
      {/* Logo - 必须包含 */}
      <img
        src={staticPlatformCdn('images/bailogo.png')}
        style={{
          position: 'absolute',
          zIndex: '900',
          width: '70%',
          top: '2%',
          left: '15%',
        }}
      />
      
      <Series>
        <Series.Sequence durationInFrames={durationInFrames}>
          <Container
            animations={[{
              type: ContainerAnimationType.ZOOM_IN_BLUR,
              config: {
                animationDelay: durationInFrames,
                animationDuration: 45,
              },
            }]}
          >
            <AbsoluteFill>
              {/* 主视频 */}
              <OffthreadVideo
                style={{
                  height: '100%',
                  width: '100%',
                  objectFit: 'cover',
                }}
                src={src}
              />
            </AbsoluteFill>
            
            <AbsoluteFill>
              {/* 脚本文本 */}
              {segmentationArray.map((startTime, index) => (
                <Sequence
                  key={index}
                  from={startTime}
                  durationInFrames={segmentationArray[index + 1] - startTime || 60}
                >
                  <AnimationText
                    baseProps={{
                      content: segmentationArrayKeyWords[index]?.[0] || '',
                      position: textPosition,
                    }}
                    effects={[{
                      type: TextEffectType.OUTLINE,
                      config: {
                        outlineColor: neutralColors[5],
                        thickness: 5,
                      },
                    }]}
                    animations={[{
                      type: TextAnimationType.POP,
                      config: { durationInFrames: 30, trigger: 'onEnter' },
                    }]}
                  />
                </Sequence>
              ))}
              
              {/* CTA - 最后3秒 */}
              <Sequence
                from={durationInFrames - 90}
                durationInFrames={90}
              >
                {/* CTA 组件 */}
              </Sequence>
            </AbsoluteFill>
          </Container>
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
```

---

## 文件位置

创建的模板应放在：
```
modules/motion-editor/src/remotion/VideoTemplate/{TemplateName}/index.tsx
```

如果使用 JSON 配置：
```
modules/motion-editor/src/remotion/VideoTemplate/{TemplateName}/composition.json
```

---

## 参考资源

| 文件 | 说明 |
|------|------|
| `references/animation_components.md` | 完整的动画组件列表和说明 |
| `references/component_structure.md` | 组件结构规范和创建指南 |
| `references/template_patterns.md` | 模板模式和最佳实践 |
| `references/layout_guidelines.md` | 布局和样式指南 |
| `scripts/generate_template.py` | 模板生成脚本 |

---

## 注意事项

1. **保持一致性**：新模板应与现有模板保持风格一致
2. **性能考虑**：避免过度使用复杂动画，注意性能优化
3. **响应式设计**：确保在不同尺寸下正常工作
4. **错误处理**：在 `calculateMetadata` 中添加错误处理
5. **类型安全**：使用 TypeScript 和 zod schema 确保类型安全
6. **脚本数量限制**：超过5个的脚本不要出现在画面中部
7. **颜色使用**：所有颜色必须从 `@/Utils/Color` 导入，禁止硬编码
8. **动画组件参考**：选择组件时必须参考 `animation_components.json`
9. **CTA 位置**：CTA 必须在视频结尾后3秒内显示
10. **Logo 注入**：每个模板必须添加 Logo，zIndex 设为 900
