# Animation Components 参考

**重要**：本文档提供组件概览，但**必须**参考 `modules/motion-editor/src/remotion/animation_components.json` 获取完整的组件信息。该 JSON 文件包含：
- 所有可用组件的完整列表
- 每个组件的 tags（标签）
- 每个组件的 intent（用途说明）
- 每个组件的 slots（插槽配置）
- 每个组件的结构类型（structure_type）

在选择动画组件时，**必须**查看 `animation_components.json` 文件进行匹配。

## 组件分类

### 1. 文本组件

#### Anim_Text_01
- **组件名**: AnimationText
- **路径**: `modules/motion-editor/src/remotion/AnimateComponent/Text`
- **用途**: 文字动画组件，支持多种文字特效和动画效果
- **常用配置**:
  ```typescript
  {
    baseProps: {
      content: string,
      position: [number, number] // [x%, y%]
    },
    effects: [
      {
        type: TextEffectType.OUTLINE | SHADOW | GLITCH | NEON | HOLLOW,
        config: {...}
      }
    ],
    animations: [
      {
        type: TextAnimationType.POP | TYPEWRITER | SPLIT_TEXT | RING_PAN | ...,
        config: {...}
      }
    ]
  }
  ```

#### Anim_SerialText_01
- **组件名**: SerialTextAnimation
- **用途**: 序列文本动画，支持按时间序列显示文本
- **配置**: 支持多个文本按时间顺序显示，可配置高亮效果

### 2. 容器组件

#### Anim_Container_01
- **组件名**: Container
- **用途**: 容器组件，为子元素提供动画包装和布局控制
- **常用动画类型**:
  - `ZOOM_IN_BLUR`: 缩放模糊
  - `ZOOM_TO_GRID_CELL`: 缩放到网格单元
  - `MASK_SHOW`: 遮罩显示
  - `ITEM_PRESS_DOWN`: 按下效果

### 3. 装饰组件

#### Anim_AgencyInfo_01
- **用途**: 展示机构信息，包含机构名称和头像
- **Slots**: `agencyName`, `agencyAvatar`

#### Anim_VideoGrid_01
- **用途**: 网格布局展示多个视频（4个或6个）
- **Slots**: `urls`

#### Anim_VideoTransform_01
- **用途**: 视频旋转轮播效果
- **Slots**: `highlights`, `textList`, `start`, `duration`, `lang`

#### Anim_FireworkParticles_01
- **用途**: 烟花粒子动画，从底部中心向上半圆形扩散
- **配置**: 
  ```typescript
  {
    animation: {
      config: {
        startTime: number,
        particleCount: number
      }
    }
  }
  ```

#### Anim_ExpandingCircleMask_01
- **用途**: 圆形扩展遮罩动画
- **配置**:
  ```typescript
  {
    animation: {
      config: {
        bgImage: string,
        center: [number, number],
        startTime: number,
        duration: number,
        pauseMs: number,
        pauseRadius: number
      }
    }
  }
  ```

#### Anim_DoubleBorder_01
- **用途**: 双重边框动画
- **配置**:
  ```typescript
  {
    animation: {
      config: {
        durationInFrames: number,
        borderColor: string,
        secondBorderColor: string,
        borderWidth: number,
        borderRadius: number,
        gap: number
      }
    }
  }
  ```

#### Anim_ExpandingBox_01
- **用途**: 扩展盒子动画，三个盒子从中心扩展出现

### 4. 视频组件

#### Anim_VideoGrid_01
- **用途**: 视频网格布局（4个或6个视频）

#### Anim_VideoTransform_01
- **用途**: 视频旋转轮播

#### Anim_RandomCutVideo_01
- **用途**: 随机选择切片段视频播放
- **配置**: `seed`, `style`

#### Anim_RandomSwitchSceneVideo_01
- **用途**: 随机选择场景切换转场视频
- **配置**: `seed`, `style`, `speed`

#### Anim_RandomCTAEndVideo_01
- **用途**: 随机选择CTA结束视频
- **配置**: `seed`, `style`

#### Anim_LoopableOffthreadVideo_01
- **用途**: 可循环的离线视频组件
- **配置**: `src`, `startFrom`, `loop`, `style`

### 5. 效果组件

#### Anim_ParticleExplosion_01
- **用途**: 粒子爆炸效果
- **配置**: `particleColor`, `particleCount`, `particleShape`, `posX`, `posY` 等

### 6. 其他组件

#### Anim_Lottie_01
- **用途**: Lottie动画组件，播放JSON格式的矢量动画

#### Anim_ImageSeries_01
- **用途**: 图片序列组件，按帧顺序播放一系列图片

## 组件选择策略

1. **根据用途选择**：
   - 文本展示 → `Anim_Text_01` 或 `Anim_SerialText_01`
   - 视频展示 → `Anim_VideoGrid_01`, `Anim_VideoTransform_01` 等
   - 装饰效果 → `Anim_FireworkParticles_01`, `Anim_ExpandingCircleMask_01` 等

2. **根据结构类型选择**：
   - 关键词动画 → `Anim_Text_01`, `Anim_SerialText_01`, `Anim_BubbleBreakout_01`
   - 素材切片 → `Anim_VideoGrid_01`, `Anim_VideoTransform_01` 等
   - 氛围动画 → `Anim_FireworkParticles_01`, `Anim_LikesAnimation_01` 等
   - 语义动画 → `Anim_Container_01` 及其子动画

3. **查看 tags 和 intent**：
   每个组件都有 `tags` 和 `intent` 字段，可以帮助理解组件的用途。

## 完整组件列表

查看 `modules/motion-editor/src/remotion/animation_components.json` 获取完整的组件列表和详细信息。


