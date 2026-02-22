# 组件结构规范

当需要创建新的动画组件时，参考本文档了解组件结构规范。

## 组件目录结构

```
modules/motion-editor/src/remotion/AnimateComponent/
├── Text/              # 文本组件
├── Container/         # 容器组件
├── Decoration/        # 装饰组件
├── Effect/            # 效果组件
├── Image/             # 图片组件
├── Lottie/            # Lottie动画
└── SerialText/        # 序列文本
```

## 组件文件结构

### 基础组件结构

```typescript
// index.tsx
import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';

export interface ComponentProps {
  // 定义 props 类型
}

export const Component: React.FC<ComponentProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  
  // 组件实现
  
  return (
    <div style={{...}}>
      {/* 组件内容 */}
    </div>
  );
};
```

### 装饰组件示例

参考 `modules/motion-editor/src/remotion/AnimateComponent/Decoration/FireworkParticles.tsx`:

```typescript
import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';

export interface FireworkParticlesProps {
  animation?: {
    config: {
      startTime: number;
      particleCount: number;
    };
  };
  style?: React.CSSProperties;
}

export const FireworkParticles: React.FC<FireworkParticlesProps> = ({
  animation,
  style,
}) => {
  const frame = useCurrentFrame();
  const { config } = animation || { config: { startTime: 0, particleCount: 36 } };
  
  // 实现逻辑
  
  return (
    <div style={style}>
      {/* 粒子效果 */}
    </div>
  );
};
```

## 在 animation_components.json 中注册

创建组件后，需要在 `animation_components.json` 中添加条目：

```json
{
  "id": "Anim_NewComponent_01",
  "component": "NewComponent",
  "file_path": "modules/motion-editor/src/remotion/AnimateComponent/Decoration",
  "tags": ["tag1", "tag2", "tag3"],
  "structure_type": "氛围动画", // 或 "关键词动画", "素材切片", "语义动画"
  "slots": ["slot1", "slot2"],
  "intent": "组件用途的简短描述",
  "slots_data": {
    "slot1": "default_value",
    "slot2": "default_value"
  },
  "styles": {
    "position": "absolute",
    "width": "100%",
    "height": "100%"
  }
}
```

## 在 MasterComposition.tsx 中注册

在 `MasterComposition.tsx` 的 `COMPONENT_MAP` 中添加映射：

```typescript
const COMPONENT_MAP: Record<string, React.ComponentType<any>> = {
  // ... 现有组件
  Anim_NewComponent_01: NewComponent,
};
```

## 组件类型分类

### 1. 文本组件 (Text)
- 位置: `AnimateComponent/Text/`
- 特点: 处理文本显示和动画
- 示例: `AnimationText`

### 2. 容器组件 (Container)
- 位置: `AnimateComponent/Container/`
- 特点: 包装其他组件，提供布局和动画
- 示例: `Container`

### 3. 装饰组件 (Decoration)
- 位置: `AnimateComponent/Decoration/`
- 特点: 提供视觉效果和装饰元素
- 示例: `FireworkParticles`, `ExpandingCircleMask`, `DoubleBorder`

### 4. 效果组件 (Effect)
- 位置: `AnimateComponent/Effect/`
- 特点: 提供特殊效果
- 示例: `ParticleExplosion`

### 5. 视频组件 (Compoment)
- 位置: `modules/motion-editor/src/remotion/Compoment/`
- 特点: 处理视频播放和切换
- 示例: `RandomCutVideo`, `RandomSwitchSceneVideo`

## 创建新组件的步骤

1. **确定组件类型和位置**
   - 根据功能选择合适的分组
   - 创建组件文件

2. **实现组件逻辑**
   - 使用 Remotion hooks (`useCurrentFrame`, `useVideoConfig`)
   - 实现动画效果
   - 处理 props

3. **注册组件**
   - 在 `animation_components.json` 中添加条目
   - 在 `MasterComposition.tsx` 中添加映射（如需要）

4. **测试组件**
   - 在模板中使用新组件
   - 验证功能和性能

## 最佳实践

1. **保持一致性**: 遵循现有组件的命名和结构规范
2. **性能优化**: 避免不必要的重渲染，合理使用 `useMemo` 和 `useCallback`
3. **类型安全**: 使用 TypeScript 定义清晰的类型
4. **可配置性**: 通过 props 提供足够的配置选项
5. **文档**: 在 `intent` 字段中清晰描述组件用途






