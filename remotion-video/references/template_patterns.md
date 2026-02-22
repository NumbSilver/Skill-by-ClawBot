# 模板模式和最佳实践

本文档总结了创建视频模板的常见模式和最佳实践。

## 模板基本结构

### 1. 标准模板结构

```typescript
import {
  AbsoluteFill,
  OffthreadVideo,
  Series,
  CalculateMetadataFunction,
  Sequence,
  useVideoConfig,
  useCurrentFrame,
  interpolate,
  Audio,
  staticFile,
} from 'remotion';
import { z } from 'zod';
import { getVideoMetadata } from '@remotion/media-utils';
import AnimationText from '@/remotion/AnimateComponent/Text';
import Container from '@/remotion/AnimateComponent/Container';
import { primaryColors, rgbaColor } from '@/Utils/Color';
import { staticPlatformCdn } from '@/Utils/cdn';
// ... 其他导入

// Schema 定义
export const TemplateNameSchema = z.object({
  src: z.string(),
  composition: z.string().optional(),
  endSrc: z.string(),
  segmentationArray: z.array(z.number()),
  segmentationArrayKeyWords: z.array(z.array(z.string())),
  _seed: z.number().optional(),
});

// 全局元数据
const globalMeta = {
  mainDuration: 0,
  endDuration: 0,
};

// 元数据计算函数
export const calculateTemplateNameMetadata: CalculateMetadataFunction<
  z.infer<typeof TemplateNameSchema>
> = async ({ props }) => {
  const fps = 30;
  try {
    const metadata = await getVideoMetadata(props.src);
    globalMeta.mainDuration = Math.floor(metadata.durationInSeconds * fps);
    return {
      fps,
      durationInFrames: globalMeta.mainDuration + 50,
    };
  } catch (error) {
    console.error('获取视频元数据失败:', error);
    return {
      fps,
      durationInFrames: 1630, // 默认值
    };
  }
};

// 主组件
export const TemplateName: React.FC<
  z.infer<typeof TemplateNameSchema>
> = ({
  src,
  endSrc,
  segmentationArray = _segmentationArray,
  segmentationArrayKeyWords = _segmentationArrayKeyWords,
}) => {
  const { width, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* Logo - 必须包含在每个模板中 */}
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
            {/* 模板内容 */}
          </Container>
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
```

## 脚本布局规则

### 脚本数量判断和位置选择

```typescript
const scriptCount = segmentationArrayKeyWords.length;

// 如果脚本数量超过5个，避免使用画面中部
if (scriptCount > 5) {
  // 使用顶部或底部位置
  baseProps={{
    position: [50, 25],  // 顶部
    // 或
    // position: [50, 75],  // 底部
  }}
} else {
  // 5个或更少可以使用中部
  baseProps={{
    position: [50, 50],  // 中部
  }}
}
```

### 推荐的脚本位置

- **顶部区域**：`position: [50, 20-30]` - 适合标题和开场
- **中部区域**：`position: [50, 50]` - 仅当脚本数量 ≤ 5 时使用
- **底部区域**：`position: [50, 70-80]` - 适合CTA和结尾
- **左右两侧**：`position: [25-35, 50]` 或 `[65-75, 50]` - 适合辅助信息

## 常见模式

### 1. 主视频 + 装饰元素

```typescript
<AbsoluteFill>
  {/* 主视频 */}
  <OffthreadVideo
    src={src}
    style={{
      height: '100%',
      width: '100%',
      objectFit: 'cover',
    }}
  />
  
  {/* 装饰元素 */}
  <Sequence from={segmentationArray[0]} durationInFrames={60}>
    <AnimationText {...textProps} />
  </Sequence>
</AbsoluteFill>
```

### 2. 分段内容展示

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
        position: [50, 50],
      }}
    />
  </Sequence>
))}
```

### 3. 转场效果

```typescript
{/* 场景切换转场 */}
<Sequence
  from={segmentationArray[2]}
  durationInFrames={30}
>
  <RandomSwitchSceneVideo
    seed={seed}
    style={{ width: '100%', height: '100%' }}
  />
</Sequence>

{/* 圆形扩展遮罩 */}
<ExpandingCircleMask
  animation={{
    config: {
      bgImage: staticFile('background_line.png'),
      center: [50, 35],
      startTime: segmentationArray[2],
      duration: 140,
      pauseMs: 100,
      pauseRadius: 370,
    },
  }}
/>
```

### 4. 结束CTA

```typescript
<Sequence
  from={segmentationArray[segmentationArray.length - 1]}
  durationInFrames={120}
>
  <RandomCTAEndVideo
    seed={seed}
    style={{ width: '100%', height: '100%' }}
  />
</Sequence>
```

## 布局模式

### 1. 居中布局

```typescript
style={{
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
}}
```

### 2. 全屏覆盖

```typescript
style={{
  position: 'absolute',
  width: '100%',
  height: '100%',
}}
```

### 3. 响应式定位

```typescript
style={{
  position: 'absolute',
  top: '8%',
  left: '15%',
  width: '70%',
  height: '13%',
}}
```

## 动画时序控制

### 1. 基于 segmentationArray

```typescript
const maxSegmentationArray = Math.min(segmentationArray.length, 7);

{maxSegmentationArray > 1 && (
  <Sequence from={segmentationArray[1]} durationInFrames={50}>
    {/* 内容 */}
  </Sequence>
)}
```

### 2. 相对时间计算

```typescript
// 在某个分段后延迟出现
<Sequence
  from={segmentationArray[2] + 20}
  durationInFrames={110}
>
  {/* 内容 */}
</Sequence>
```

### 3. 动态缩放

```typescript
const scale = interpolate(
  frame,
  [0, 10, segmentationArray[1], segmentationArray[1] + 60],
  [2, 1, 1, 1.3],
  { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
);
```

## 颜色和样式

**重要**：所有颜色必须从 `@/Utils/Color` 导入，禁止硬编码颜色值。

### 1. 使用项目颜色系统

```typescript
import { primaryColors, secondaryColors, neutralColors, rgbaColor } from '@/Utils/Color';

// 使用主色
color: primaryColors[0]
backgroundColor: primaryColors[1]

// 使用半透明色
backgroundColor: rgbaColor(primaryColors[1], 0.7)

// 使用中性色（替代硬编码的黑色和白色）
backgroundColor: neutralColors[0]  // 黑色
color: neutralColors[5]  // 白色

// 禁止使用硬编码颜色
// ❌ backgroundColor: '#000'
// ❌ color: 'white'
// ✅ backgroundColor: neutralColors[0]
// ✅ color: neutralColors[5]
```

### 2. 字体使用

```typescript
import { TikTokSansText } from '@/Utils/load-font';

style={{
  fontFamily: TikTokSansText,
  fontSize: 80,
  fontWeight: 1000,
}}
```

### 3. 文本效果

```typescript
effects={[
  {
    type: TextEffectType.OUTLINE,
    config: {
      outlineColor: 'white',
      thickness: 5,
    },
  },
  {
    type: TextEffectType.SHADOW,
    config: {
      color: primaryColors[1],
    },
  },
]}
```

## 性能优化

1. **使用 OffthreadVideo**: 对于长视频，使用 `OffthreadVideo` 而不是 `Video`
2. **合理使用 Sequence**: 避免创建过多的 Sequence，合理控制数量
3. **条件渲染**: 使用条件判断避免不必要的渲染
4. **静态资源**: 使用 `staticFile` 加载静态资源

## 错误处理

```typescript
export const calculateMetadata: CalculateMetadataFunction<...> = async ({ props }) => {
  const fps = 30;
  try {
    const metadata = await getVideoMetadata(props.src);
    return {
      fps,
      durationInFrames: Math.floor(metadata.durationInSeconds * fps) + 50,
    };
  } catch (error) {
    console.error('获取视频元数据失败:', error);
    // 返回默认值，避免应用崩溃
    return {
      fps,
      durationInFrames: 1630,
    };
  }
};
```

## 模板元信息

可以添加模板元信息（可选）：

```typescript
export const TemplateNameTemplateMeta = {
  zh: {
    overview: '模板概述',
    useCases: ['用例1', '用例2'],
    keywords: [],
  },
  en: {
    overview: 'Template overview',
    useCases: ['Use case 1', 'Use case 2'],
    keywords: [],
  },
};
```


