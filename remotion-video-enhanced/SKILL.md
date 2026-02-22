---
name: remotion-video-enhanced
description: Enhanced Remotion video template creation skill with intelligent component matching, layout automation, and best practices. Use when creating video templates, matching animations to scripts, generating Remotion components, or implementing video generation workflows with Remotion.js.
---

# Remotion Video Template Creator (Enhanced)

Create professional Remotion video templates with intelligent component matching and automated best practices.

## Quick Start

```bash
# Generate a new template
python scripts/generate_template.py TemplateName --path ./VideoTemplate
```

## Core Workflow

### 1. Analyze Requirements
- Template purpose and scene type
- Content types (text, video, images)
- Desired animation style
- Script segmentation data

### 2. Select Components

**Decision Tree:**
```
Need what type of content?
├── Text display
│   ├── Single text → Anim_Text_01
│   └── Sequential → Anim_SerialText_01
├── Video display
│   ├── Grid (4/6 videos) → Anim_VideoGrid_01
│   ├── Rotation carousel → Anim_VideoTransform_01
│   ├── Random clips → Anim_RandomCutVideo_01
│   └── Scene transitions → Anim_RandomSwitchSceneVideo_01
├── Decorations
│   ├── Fireworks → Anim_FireworkParticles_01
│   ├── Circle mask → Anim_ExpandingCircleMask_01
│   ├── Double border → Anim_DoubleBorder_01
│   └── Agency info → Anim_AgencyInfo_01
└── Container → Anim_Container_01
```

**Reference:** See [references/animation_components.md](references/animation_components.md) for full component catalog.

### 3. Build Template

**Required Structure:**
```typescript
import { AbsoluteFill, Series, Sequence, OffthreadVideo } from 'remotion';
import { z } from 'zod';
import { getVideoMetadata } from '@remotion/media-utils';
import { primaryColors, neutralColors, rgbaColor } from '@/Utils/Color';
import { staticPlatformCdn } from '@/Utils/cdn';
import AnimationText from '@/remotion/AnimateComponent/Text';
import Container from '@/remotion/AnimateComponent/Container';

// Schema
export const TemplateSchema = z.object({
  src: z.string(),
  composition: z.string().optional(),
  endSrc: z.string(),
  segmentationArray: z.array(z.number()),
  segmentationArrayKeyWords: z.array(z.array(z.string())),
  _seed: z.number().optional(),
});

// Metadata calculation
export const calculateTemplateMetadata = async ({ props }) => {
  const fps = 30;
  const metadata = await getVideoMetadata(props.src);
  return {
    fps,
    durationInFrames: Math.floor(metadata.durationInSeconds * fps) + 50,
  };
};

// Component
export const Template = ({ src, segmentationArray, segmentationArrayKeyWords }) => {
  const { durationInFrames } = useVideoConfig();
  const scriptCount = segmentationArrayKeyWords.length;

  return (
    <AbsoluteFill style={{ backgroundColor: neutralColors[0] }}>
      {/* Logo - REQUIRED */}
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
      {/* Content */}
    </AbsoluteFill>
  );
};
```

## Critical Rules

### 1. Logo Injection (MANDATORY)
```typescript
// Every template MUST include this
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

### 2. Color System (NO HARDCODING)
```typescript
// ✅ CORRECT
import { primaryColors, neutralColors, rgbaColor } from '@/Utils/Color';
color: primaryColors[0]
backgroundColor: rgbaColor(primaryColors[1], 0.7)
textColor: neutralColors[5]  // white

// ❌ FORBIDDEN
color: '#000'
backgroundColor: 'white'
```

### 3. Script Position Rules
```typescript
const scriptCount = segmentationArrayKeyWords.length;

// If > 5 scripts, AVOID center position
const position = scriptCount > 5 
  ? [50, 25]  // Top position
  : [50, 50]; // Center (only for ≤5 scripts)

// Position options:
// - Top: [50, 20-30]
// - Center: [50, 50] (≤5 scripts only)
// - Bottom: [50, 70-80]
// - Left: [25-35, 50]
// - Right: [65-75, 50]
```

### 4. CTA Timing
```typescript
// CTA must appear in last 3 seconds
const ctaStartFrame = durationInFrames - 90; // 90 frames = 3 seconds at 30fps
```

## Animation Patterns

### Text Animation
```typescript
<AnimationText
  baseProps={{
    content: segmentationArrayKeyWords[0]?.[0],
    position: [50, 50],
  }}
  effects={[{
    type: TextEffectType.OUTLINE,
    config: { outlineColor: neutralColors[5], thickness: 5 },
  }]}
  animations={[{
    type: TextAnimationType.POP,
    config: { durationInFrames: 30, trigger: 'onEnter' },
  }]}
/>
```

### Container Animation
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
  {/* Child content */}
</Container>
```

### Segmentation Display
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
        position: [50, scriptCount > 5 ? 25 : 50],
      }}
    />
  </Sequence>
))}
```

## Reference Files

| File | Purpose |
|------|---------|
| [animation_components.md](references/animation_components.md) | Full component catalog |
| [component_structure.md](references/component_structure.md) | Creating new components |
| [template_patterns.md](references/template_patterns.md) | Best practices & patterns |
| [layout_guidelines.md](references/layout_guidelines.md) | Layout & styling rules |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate_template.py` | Generate template scaffold |

## Best Practices

1. **Keep templates consistent** - Follow existing patterns
2. **Optimize performance** - Use `OffthreadVideo` for long videos
3. **Handle errors** - Add try/catch in `calculateMetadata`
4. **Test responsiveness** - Use percentage positioning
5. **Reference animation_components.json** - For component selection

## Output Location

```
modules/motion-editor/src/remotion/VideoTemplate/{TemplateName}/index.tsx
```
