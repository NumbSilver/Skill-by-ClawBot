# 布局和样式指南

本文档提供了视频模板的布局和样式规范。

## 布局原则

### 1. 容器结构

标准的三层结构：
```
AbsoluteFill (根容器)
  └─ Series (序列容器)
      └─ Series.Sequence (主序列)
          └─ Container (动画容器)
              └─ 内容元素
```

### 2. 定位系统

使用百分比定位，确保响应式：

```typescript
// 居中
position: [50, 50]  // [x%, y%]

// 自定义位置
style={{
  position: 'absolute',
  top: '8%',
  left: '15%',
  width: '70%',
  height: '13%',
}}
```

## Logo 注入规则

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

**规则**：
- Logo 必须使用 `staticPlatformCdn('images/bailogo.png')` 路径
- zIndex 设置为 900，确保在所有内容之上
- 位置固定在顶部（top: '2%', left: '15%'）
- 宽度为 70%

## 颜色系统

**重要**：所有颜色必须从 `@/Utils/Color` 导入，禁止硬编码颜色值。

### 主色

```typescript
import { primaryColors, rgbaColor } from '@/Utils/Color';

// primaryColors[0]: 第一个主色
// primaryColors[1]: 第二个主色
// primaryColors[2]: 第三个主色

// 使用半透明色
rgbaColor(primaryColors[1], 0.7)
```

### 半透明色

```typescript
import { rgbaColor } from '@/Utils/Color';

// 创建半透明色
rgbaColor(primaryColors[1], 0.7)
```

### 常用颜色值

**禁止硬编码，必须使用导入的颜色**：

```typescript
import { primaryColors, neutralColors, rgbaColor } from '@/Utils/Color';

// 背景色: neutralColors[0] (黑色)
// 文字色: neutralColors[5] (白色) 或 primaryColors[0]
// 强调色: primaryColors[1]
// 半透明背景: rgbaColor(primaryColors[1], 0.7)
```

## 字体系统

### 主要字体

```typescript
import { TikTokSansText } from '@/Utils/load-font';

style={{
  fontFamily: TikTokSansText,
  fontSize: 80,        // 根据场景调整
  fontWeight: 1000,     // 粗体
}}
```

### 字体大小建议

- 标题: 90-120px
- 正文: 60-80px
- 小字: 40-50px

## 文本样式

### 基础文本样式

```typescript
style={{
  transform: 'skew(50deg)',      // 倾斜效果（可选）
  display: 'inline-block',
  color: 'white',
  fontSize: 80,
  fontWeight: 1000,
  zIndex: 100,
  width: '100%',
}}
```

### 带背景的文本

```typescript
style={{
  backgroundColor: 'rgba(0, 215, 211, 0.7)',
  borderRadius: 30,
  padding: 20,
  color: 'white',
  fontSize: 80,
  fontWeight: 700,
  fontFamily: TikTokSansText,
  width: '90%',
}}
```

### 文本效果

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

## 视频样式

### 全屏视频

```typescript
style={{
  height: '100%',
  width: '100%',
  objectFit: 'cover',
}}
```

### 带缩放的视频

```typescript
style={{
  height: '100%',
  width: '100%',
  objectFit: 'cover',
  transform: `scale(${scale})`,
  transformOrigin: 'center center',
}}
```

### 部分区域视频

```typescript
style={{
  width: '69%',
  height: '67%',
  top: '61%',
  position: 'absolute',
  left: '49.5%',
  borderRadius: '30px 20px',
  border: '10px solid animatedBorderColor',
  transform: 'translate(-50%,-50%)',
}}
```

## 装饰元素样式

### 边框装饰

```typescript
style={{
  width: '100%',
  height: '100%',
  margin: 'auto',
  boxShadow: '0 0 20px 0 rgba(82, 173, 212, 0.5)',
  borderRadius: 30,
}}
```

### 背景装饰

```typescript
style={{
  position: 'absolute',
  width: '100%',
  height: '100%',
  background: 'url(bg.png)',  // 或使用渐变
}}
```

## 动画时序

### 标准时序

- 文本出现: 30-60 帧
- 转场效果: 30 帧
- 装饰动画: 45-90 帧
- 结束CTA: 90-120 帧

### 延迟策略

```typescript
// 在分段开始后延迟
from={segmentationArray[2] + 20}

// 在分段结束前开始
from={segmentationArray[segmentationArray.length - 1] - 90}
```

## 响应式考虑

### 使用百分比

始终使用百分比而不是固定像素值（除了字体大小）。

### 居中技巧

```typescript
// 方法1: 使用 position prop
baseProps={{
  position: [50, 50],
}}

// 方法2: 使用 transform
style={{
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
}}
```

## 层级管理 (z-index)

```typescript
// 背景层
zIndex: 0

// 内容层
zIndex: 100

// 装饰层
zIndex: 200

// 顶层
zIndex: 500
```

## 脚本布局规则

**重要限制**：如果脚本数量超过5个，这些脚本**不能**出现在画面中部（position: [50, 50]），会影响视觉效果。

### 脚本位置建议

当脚本数量 > 5 时，使用以下位置：

```typescript
// 顶部区域（推荐）
baseProps={{
  position: [50, 20],  // 或 [50, 25], [50, 30]
}}

// 底部区域（推荐）
baseProps={{
  position: [50, 75],  // 或 [50, 78], [50, 80]
}}

// 左侧区域
baseProps={{
  position: [30, 50],  // 或 [25, 50], [35, 50]
}}

// 右侧区域
baseProps={{
  position: [70, 50],  // 或 [65, 50], [75, 50]
}}
```

### 脚本数量判断

```typescript
const scriptCount = segmentationArrayKeyWords.length;

// 如果超过5个，避免使用 position: [50, 50]
if (scriptCount > 5) {
  // 使用顶部或底部位置
  position: [50, 25]  // 顶部
  // 或
  position: [50, 75]  // 底部
}
```

## 常见布局模式

### 1. 顶部标题 + 中间内容

```typescript
// 顶部标题
<AnimationText
  baseProps={{
    position: [50, 20],  // 顶部
  }}
/>

// 中间内容
<AnimationText
  baseProps={{
    position: [50, 50],  // 中间
  }}
/>
```

### 2. 底部CTA

```typescript
<AnimationText
  baseProps={{
    position: [50, 78],  // 底部
  }}
/>
```

### 3. 左右分栏

```typescript
// 左侧
style={{
  position: 'absolute',
  left: '10%',
  width: '40%',
}}

// 右侧
style={{
  position: 'absolute',
  right: '10%',
  width: '40%',
}}
```

## 最佳实践

1. **保持一致性**: 使用统一的颜色、字体和间距
2. **层次清晰**: 使用 z-index 管理层级关系
3. **响应式**: 使用百分比和相对单位
4. **性能**: 避免过度使用复杂样式和效果
5. **可读性**: 确保文字清晰可读，对比度足够


