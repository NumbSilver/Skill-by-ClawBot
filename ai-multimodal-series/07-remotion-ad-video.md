# 07 - 视频生成结合 Remotion 生成可编辑广告视频

## 核心论点
> **AI 生成视频的终极痛点是「不可编辑」。Remotion 工作流让广告视频从「一次性生成」变为「可编程、可迭代、可 A/B 测试」，实现真正的工业化生产。**

---

## 一、为什么需要可编辑的视频工作流？(10min)

### 1.1 传统 AI 视频的局限
```
当前 AI 视频生成流程:
文本/图片 → AI 模型 → MP4 视频 → ❌ 结束

问题:
1. 无法修改：发现错别字？重新生成整个视频
2. 无法 A/B 测试：想换背景音乐？重新生成
3. 无法批量变体：10 个 product SKU？生成 10 次
4. 无法模板化：类似广告要重做，无法复用
5. 无法精确控制：品牌颜色/字体/LOGO 位置无法保证一致

结果:
- 每次修改成本高 (时间 + API 费用)
- 无法快速迭代优化
- 风格一致性难以保证
- 不适合企业级规模化需求
```

### 1.2 Remotion 的优势
```
Remotion 核心理念：视频即代码 (Video as Code)

传统视频编辑:          Remotion:
┌─────────────┐        ┌─────────────┐
│  时间轴界面  │        │   React 代码 │
│  手动拖拽    │        │  组件化组合  │
│  导出 MP4    │        │  渲染 MP4    │
└─────────────┘        └─────────────┘
  难以复用                 完全可复用
  手动操作                 自动化
  单次使用                 模板化

Remotion + AI 工作流:
AI 生成素材 → Remotion 组合 → 可编程编辑 → 批量输出
    ↓           ↓             ↓            ↓
  场景视频     时间轴        修改参数      100 个变体
  角色视频     转场特效      替换素材      不同尺寸
  背景音乐     字幕动画      A/B 测试      多平台适配

核心价值:
✅ 可编辑：修改代码而非重新生成
✅ 可复用：模板化，一套代码生成无数视频
✅ 可自动化：CI/CD 流水线自动生成视频
✅ 可版本控制：Git 管理视频版本
✅ 可 A/B 测试：快速生成多个版本测试效果
```

### 1.3 应用场景与 ROI
```
场景 1: 电商产品广告
需求：100 个 SKU，每个需要 3 个版本 (15s/30s/60s)
传统 AI 方案:
  - 生成次数：100 × 3 = 300 次
  - 成本：300 × $2 = $600
  - 修改成本：改一个元素 = 重新生成 300 次

Remotion 方案:
  - 生成素材：100 个产品图 → 100 次 AI 生成 ($200)
  - 模板开发：4 小时 (一次性)
  - 批量渲染：100 × 3 = 300 次 (本地渲染，$0)
  - 修改成本：改代码，重新渲染 (免费)
  - 总成本：$200 + 人力
  - 节省：60%+ 成本，90%+ 修改时间

场景2: 社交媒体广告 A/B 测试
需求：同一广告，测试 5 个开场 + 4 个文案 + 3 个音乐 = 60 个变体
传统方案：生成 60 次，$120，耗时 2 天
Remotion 方案：生成素材 1 次 ($10) + 批量渲染 60 次 (免费)，耗时 2 小时

场景 3: 多平台适配
需求：同一广告，适配抖音 (9:16)、YouTube (16:9)、Instagram (1:1)
传统方案：每个尺寸重新生成，3 倍成本
Remotion 方案：改一个参数，批量渲染，0 额外成本
```

---

## 二、Remotion 基础与架构 (10min)

### 2.1 Remotion 核心概念
```
Remotion = React + 视频渲染引擎

核心组件:
┌─────────────────────────────────────────┐
│  Composition (合成)                      │
│    └─ 视频的「画布」，定义分辨率、时长、FPS  │
│                                          │
│    └─ 包含多个 Layer (层)                 │
│        └─ AbsoluteFill (全屏层)          │
│        └─ Video (视频片段)               │
│        └─ Audio (音频)                   │
│        └─ Title (文字标题)               │
│        └─ Image (图片)                   │
│        └─ 自定义 React 组件              │
└─────────────────────────────────────────┘

时间轴控制:
- useCurrentFrame(): 获取当前帧号
- interpolate(): 基于帧数做动画
- Easing: 缓动函数 (ease-in-out 等)

渲染流程:
1. 开发：remotion studio (浏览器预览)
2. 渲染：remotion render (输出 MP4)
3. 批量：remotion batch (多个变体)
```

### 2.2 环境搭建
```bash
# 1. 创建 Remotion 项目
npx create-remotion@latest ai-ad-video
cd ai-ad-video

# 2. 安装依赖
npm install @remotion/cli
npm install remotion
npm install @remotion/media-utils
npm install @remotion/zod-types

# 3. 启动开发服务器
npm run studio
# 访问 http://localhost:3000 预览

# 4. 渲染视频
npm run build -- --input=MyComposition --output=out.mp4
```

### 2.3 第一个 Remotion 组件
```tsx
// src/MyComposition.tsx
import { AbsoluteFill, useCurrentFrame } from 'remotion';

export const MyComposition = () => {
  const frame = useCurrentFrame();
  
  return (
    <AbsoluteFill style={{ backgroundColor: 'white' }}>
      {/* 基于帧数的动画 */}
      <div
        style={{
          fontSize: 100,
          textAlign: 'center',
          transform: `scale(${1 + frame * 0.01})`,
        }}
      >
        Hello Remotion!
      </div>
    </AbsoluteFill>
  );
};
```

```tsx
// src/index.tsx
import { registerRoot } from 'remotion';
import { RemotionRoot } from './RemotionRoot';

registerRoot(RemotionRoot);

// src/RemotionRoot.tsx
import { Composition } from 'remotion';
import { MyComposition } from './MyComposition';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="MyComposition"
        component={MyComposition}
        durationInFrames={150}  // 5 秒 @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

---

## 三、AI + Remotion 工作流设计 (15min)

### 3.1 整体架构
```
┌─────────────────────────────────────────────────────┐
│              AI + Remotion 工作流                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐                                  │
│  │  输入数据     │                                  │
│  │  - 产品图     │                                  │
│  │  - 产品文案   │                                  │
│  │  - 品牌规范   │                                  │
│  └──────┬───────┘                                  │
│         │                                           │
│         ↓                                           │
│  ┌──────────────┐    ┌──────────────┐              │
│  │  AI 素材生成  │    │  模板开发     │              │
│  │  - 场景视频   │    │  - React 组件 │              │
│  │  - 角色视频   │◄───┤  - 动画逻辑  │              │
│  │  - 背景音乐   │    │  - 参数配置  │              │
│  └──────┬───────┘    └──────┬───────┘              │
│         │                    │                       │
│         └────────┬───────────┘                       │
│                  ↓                                    │
│         ┌────────────────┐                           │
│         │ Remotion 合成   │                           │
│         │ - 时间轴编排    │                           │
│         │ - 素材组合      │                           │
│         │ - 特效添加      │                           │
│         └────────┬───────┘                           │
│                  │                                    │
│         ┌────────┴────────┐                          │
│         ↓                 ↓                          │
│  ┌─────────────┐   ┌─────────────┐                  │
│  │  单视频渲染  │   │  批量渲染    │                  │
│  │  (预览/定稿) │   │  (A/B 测试)   │                  │
│  └─────────────┘   └─────────────┘                  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 3.2 可配置模板设计
```tsx
// src/templates/ProductAdTemplate.tsx
import { AbsoluteFill, Sequence, useCurrentFrame } from 'remotion';
import { ProductVideo } from './ProductVideo';
import { TitleCard } from './TitleCard';
import { CallToAction } from './CallToAction';
import type { AdConfig } from './types';

interface ProductAdTemplateProps {
  config: AdConfig;
}

export const ProductAdTemplate: React.FC<ProductAdTemplateProps> = ({
  config,
}) => {
  const frame = useCurrentFrame();
  
  return (
    <AbsoluteFill style={{ backgroundColor: config.brand.backgroundColor }}>
      {/* 开场标题 (0-2 秒) */}
      <Sequence from={0} durationInFrames={60}>
        <TitleCard
          title={config.headline}
          subtitle={config.subheadline}
          brandColor={config.brand.primaryColor}
        />
      </Sequence>
      
      {/* 产品展示 (2-8 秒) */}
      <Sequence from={60} durationInFrames={180}>
        <ProductVideo
          productImage={config.product.image}
          productVideo={config.product.video}
          features={config.product.features}
          brandColor={config.brand.primaryColor}
        />
      </Sequence>
      
      {/* 用户评价 (8-12 秒) */}
      <Sequence from={240} durationInFrames={120}>
        <Testimonial
          quote={config.testimonial.quote}
          author={config.testimonial.author}
          rating={config.testimonial.rating}
        />
      </Sequence>
      
      {/* 行动号召 (12-15 秒) */}
      <Sequence from={360} durationInFrames={90}>
        <CallToAction
          text={config.cta.text}
          link={config.cta.link}
          brandColor={config.brand.primaryColor}
        />
      </Sequence>
      
      {/* 品牌 LOGO (全程淡入) */}
      <Sequence from={420} durationInFrames={30}>
        <LogoOverlay
          logo={config.brand.logo}
          opacity={interpolate(frame, [420, 435], [0, 1])}
        />
      </Sequence>
    </AbsoluteFill>
  );
};
```

### 3.3 TypeScript 配置类型
```ts
// src/templates/types.ts
export interface AdConfig {
  // 品牌规范
  brand: {
    primaryColor: string;
    secondaryColor: string;
    backgroundColor: string;
    logo: string;  // URL 或本地路径
    font: string;
  };
  
  // 产品信息
  product: {
    name: string;
    image: string;
    video?: string;  // 可选：AI 生成的产品视频
    features: string[];
    price: string;
    originalPrice?: string;  // 原价 (用于显示折扣)
  };
  
  // 广告文案
  headline: string;
  subheadline?: string;
  testimonial: {
    quote: string;
    author: string;
    rating: number;  // 1-5
  };
  
  // 行动号召
  cta: {
    text: string;
    link: string;
  };
  
  // 视频规格
  videoSpec: {
    durationInSeconds: number;
    aspectRatio: '9:16' | '16:9' | '1:1';
    fps: number;
  };
  
  // AI 生成素材
  aiAssets?: {
    sceneVideo?: string;
    characterVideo?: string;
    backgroundMusic?: string;
  };
}

// 预设模板配置
export const PRESET_TEMPLATES = {
  'ecommerce-15s': {
    durationInSeconds: 15,
    aspectRatio: '9:16' as const,
    fps: 30,
  },
  'youtube-30s': {
    durationInSeconds: 30,
    aspectRatio: '16:9' as const,
    fps: 30,
  },
  'instagram-square': {
    durationInSeconds: 15,
    aspectRatio: '1:1' as const,
    fps: 30,
  },
};
```

### 3.4 AI 素材集成
```tsx
// src/components/ProductVideo.tsx
import { AbsoluteFill, Img, Video, useCurrentFrame } from 'remotion';
import { interpolate } from 'remotion';

interface ProductVideoProps {
  productImage: string;
  productVideo?: string;  // AI 生成的产品视频
  features: string[];
  brandColor: string;
}

export const ProductVideo: React.FC<ProductVideoProps> = ({
  productImage,
  productVideo,
  features,
  brandColor,
}) => {
  const frame = useCurrentFrame();
  
  // 如果有 AI 生成的产品视频，优先使用
  if (productVideo) {
    return (
      <AbsoluteFill>
        <Video
          src={productVideo}
          style={{ objectFit: 'cover' }}
        />
        {/* 叠加特性文字 */}
        <FeatureOverlay features={features} frame={frame} color={brandColor} />
      </AbsoluteFill>
    );
  }
  
  // 否则使用图片 + 动画
  const scale = interpolate(frame, [0, 60], [1, 1.1]);
  
  return (
    <AbsoluteFill style={{ backgroundColor: '#f5f5f5' }}>
      <Img
        src={productImage}
        style={{
          objectFit: 'contain',
          transform: `scale(${scale})`,
        }}
      />
      
      {/* 特性列表动画 */}
      {features.map((feature, index) => (
        <Sequence
          key={feature}
          from={index * 20}
          durationInFrames={40}
        >
          <FeatureItem
            text={feature}
            delay={index * 20}
            color={brandColor}
          />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

// 特性文字组件
const FeatureItem: React.FC<{ text: string; delay: number; color: string }> = ({
  text,
  delay,
  color,
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15, 40], [0, 1, 1]);
  const translateY = interpolate(frame, [0, 15], [20, 0]);
  
  return (
    <div
      style={{
        position: 'absolute',
        bottom: 100 + delay,
        left: 50,
        fontSize: 32,
        fontWeight: 'bold',
        color: color,
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      ✨ {text}
    </div>
  );
};
```

### 3.5 AI 生成背景音乐集成
```tsx
// src/components/AudioTrack.tsx
import { Audio, useCurrentFrame } from 'remotion';
import { useAudioData } from '@remotion/media-utils';

interface AudioTrackProps {
  musicUrl?: string;  // AI 生成的背景音乐
  voiceoverUrl?: string;  // AI 生成的配音
}

export const AudioTrack: React.FC<AudioTrackProps> = ({
  musicUrl,
  voiceoverUrl,
}) => {
  return (
    <>
      {/* 背景音乐 (音量 30%) */}
      {musicUrl && (
        <Audio
          src={musicUrl}
          volume={0.3}
          loop={true}
        />
      )}
      
      {/* 配音 (音量 100%) */}
      {voiceoverUrl && (
        <Audio
          src={voiceoverUrl}
          volume={1.0}
        />
      )}
    </>
  );
};

// 可视化音频波形 (可选)
export const AudioVisualizer: React.FC<{ audioSrc: string }> = ({ audioSrc }) => {
  const frame = useCurrentFrame();
  const audioData = useAudioData(audioSrc);
  
  if (!audioData) {
    return null;
  }
  
  // 获取当前帧的音频频率数据
  const frequency = audioData.frequencyData[frame];
  const barHeight = (frequency?.[0] || 0) * 2;
  
  return (
    <div
      style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: `${barHeight}px`,
        background: 'linear-gradient(to top, rgba(52, 152, 219, 0.5), transparent)',
      }}
    />
  );
};
```

---

## 四、批量生成与 A/B 测试 (12min)

### 4.1 批量渲染脚本
```ts
// scripts/batch-render.ts
import { bundle } from '@remotion/bundler';
import { renderMedia, selectComposition } from '@remotion/renderer';
import { Config } from '../src/templates/types';

async function batchRender() {
  // 1. 打包 Remotion 项目
  const bundleLocation = await bundle();
  
  // 2. 定义多个变体配置
  const variants: Config[] = [
    {
      brand: {
        primaryColor: '#FF6B6B',
        secondaryColor: '#4ECDC4',
        backgroundColor: '#FFFFFF',
        logo: '/logos/logo-red.png',
        font: 'Inter',
      },
      product: {
        name: '智能手表 X1',
        image: '/products/watch-x1.jpg',
        features: ['心率监测', '7 天续航', '50 米防水'],
        price: '¥999',
      },
      headline: '全新智能手表 X1',
      subheadline: '健康随行，智慧生活',
      testimonial: {
        quote: '用了一周，续航真的厉害！',
        author: '张女士',
        rating: 5,
      },
      cta: {
        text: '立即购买',
        link: 'https://example.com/buy',
      },
      videoSpec: {
        durationInSeconds: 15,
        aspectRatio: '9:16',
        fps: 30,
      },
    },
    // 变体 2: 不同配色
    {
      ...variants[0],
      brand: {
        ...variants[0].brand,
        primaryColor: '#3498DB',
        logo: '/logos/logo-blue.png',
      },
    },
    // 变体 3: 不同文案
    {
      ...variants[0],
      headline: '限时特惠！智能手表 X1',
      subheadline: '今日下单立减 200 元',
      product: {
        ...variants[0].product,
        price: '¥799',
        originalPrice: '¥999',
      },
    },
    // ... 更多变体
  ];
  
  // 3. 批量渲染
  for (let i = 0; i < variants.length; i++) {
    const variant = variants[i];
    const outputPath = `./outputs/ad-variant-${i + 1}.mp4`;
    
    console.log(`🎬 渲染变体 ${i + 1}/${variants.length}...`);
    
    await renderMedia({
      composition: await selectComposition({
        serveUrl: bundleLocation,
        id: 'ProductAdTemplate',
        inputProps: { config: variant },
      }),
      format: 'mp4',
      outputLocation: outputPath,
      codec: 'h264',
      crf: 23,  // 质量控制 (0-51, 越小质量越高)
    });
    
    console.log(`✅ 完成：${outputPath}`);
  }
  
  console.log(`\n🎉 批量渲染完成！共 ${variants.length} 个变体`);
}

batchRender().catch(console.error);
```

### 4.2 多平台尺寸适配
```ts
// scripts/render-multi-platform.ts
import { renderMedia } from '@remotion/renderer';

const PLATFORMS = {
  'tiktok': { width: 1080, height: 1920, aspectRatio: '9:16' },
  'youtube': { width: 1920, height: 1080, aspectRatio: '16:9' },
  'instagram': { width: 1080, height: 1080, aspectRatio: '1:1' },
  'facebook': { width: 1200, height: 628, aspectRatio: '1.91:1' },
};

async function renderForAllPlatforms(config: Config) {
  const bundleLocation = await bundle();
  
  for (const [platform, spec] of Object.entries(PLATFORMS)) {
    const outputPath = `./outputs/ad-${platform}.mp4`;
    
    // 动态修改 composition 配置
    await renderMedia({
      composition: {
        id: 'ProductAdTemplate',
        component: ProductAdTemplate,
        durationInFrames: config.videoSpec.durationInSeconds * config.videoSpec.fps,
        fps: config.videoSpec.fps,
        width: spec.width,
        height: spec.height,
        defaultProps: { config },
      },
      serveUrl: bundleLocation,
      outputLocation: outputPath,
      format: 'mp4',
      codec: 'h264',
    });
    
    console.log(`✅ ${platform}: ${outputPath}`);
  }
}
```

### 4.3 CI/CD 自动化
```yaml
# .github/workflows/render-videos.yml
name: Render AI Ad Videos

on:
  push:
    paths:
      - 'src/**'
      - 'config/**'
  workflow_dispatch:
    inputs:
      campaign:
        description: 'Campaign name'
        required: true

jobs:
  render:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install FFmpeg
        run: sudo apt-get update && sudo apt-get install -y ffmpeg
      
      - name: Download AI assets
        run: |
          # 从云存储下载 AI 生成的素材
          wget https://storage.example.com/ai-assets/product-videos.zip
          unzip product-videos.zip
      
      - name: Render videos
        run: npm run batch-render
        env:
          CAMPAIGN_NAME: ${{ github.event.inputs.campaign }}
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: rendered-videos
          path: outputs/*.mp4
      
      - name: Deploy to S3
        run: aws s3 cp outputs/ s3://my-bucket/videos/${{ github.event.inputs.campaign }}/ --recursive
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## 五、完整实战案例 (10min)

### 5.1 项目结构
```
ai-ad-video/
├── src/
│   ├── index.tsx                 # Remotion 入口
│   ├── RemotionRoot.tsx          # 注册 compositions
│   ├── templates/
│   │   ├── ProductAdTemplate.tsx # 主模板
│   │   ├── components/
│   │   │   ├── TitleCard.tsx
│   │   │   ├── ProductVideo.tsx
│   │   │   ├── Testimonial.tsx
│   │   │   ├── CallToAction.tsx
│   │   │   └── LogoOverlay.tsx
│   │   └── types.ts              # TypeScript 类型定义
│   └── styles/
│       └── global.css
├── public/
│   ├── products/                 # 产品图
│   ├── videos/                   # AI 生成视频
│   ├── audio/                    # AI 生成音频
│   └── logos/                    # 品牌 LOGO
├── scripts/
│   ├── batch-render.ts           # 批量渲染脚本
│   └── generate-thumbnails.ts    # 生成封面图
├── config/
│   ├── campaigns/
│   │   ├── campaign-001.json     # 活动配置 1
│   │   └── campaign-002.json     # 活动配置 2
│   └── brands/
│       ├── brand-a.json          # 品牌 A 规范
│       └── brand-b.json          # 品牌 B 规范
├── package.json
├── remotion.config.ts
└── README.md
```

### 5.2 活动配置文件
```json
// config/campaigns/campaign-001.json
{
  "campaignName": "双 11 特惠",
  "brand": "brand-a",
  "products": [
    {
      "sku": "WATCH-X1",
      "name": "智能手表 X1",
      "image": "/products/watch-x1.jpg",
      "video": "/videos/watch-x1-ai.mp4",
      "features": ["心率监测", "7 天续航", "50 米防水"],
      "price": "¥799",
      "originalPrice": "¥999"
    },
    {
      "sku": "EARBUDS-PRO",
      "name": "无线耳机 Pro",
      "image": "/products/earbuds-pro.jpg",
      "video": "/videos/earbuds-pro-ai.mp4",
      "features": ["主动降噪", "30 小时续航", "IPX4 防水"],
      "price": "¥599",
      "originalPrice": "¥799"
    }
  ],
  "platforms": ["tiktok", "youtube", "instagram"],
  "variants": {
    "headline": [
      "双 11 限时特惠!",
      "全年最低价!",
      "错过等一年!"
    ],
    "music": [
      "/audio/upbeat-01.mp3",
      "/audio/emotional-01.mp3"
    ]
  },
  "outputDir": "./outputs/campaign-001"
}
```

### 5.3 一键生成脚本
```bash
#!/bin/bash
# scripts/generate-campaign.sh

CAMPAIGN_CONFIG=$1

if [ -z "$CAMPAIGN_CONFIG" ]; then
  echo "用法：./generate-campaign.sh <config-file>"
  exit 1
fi

echo "🚀 开始生成广告视频..."
echo "配置文件：$CAMPAIGN_CONFIG"

# 1. 下载 AI 素材
echo "📥 下载 AI 生成素材..."
node scripts/download-ai-assets.js $CAMPAIGN_CONFIG

# 2. 生成所有变体
echo "🎬 批量渲染视频..."
node scripts/batch-render.js $CAMPAIGN_CONFIG

# 3. 生成封面图
echo "🖼️  生成封面图..."
node scripts/generate-thumbnails.js $CAMPAIGN_CONFIG

# 4. 质量检查
echo "🔍 质量检查..."
node scripts/quality-check.js $CAMPAIGN_CONFIG

echo "✅ 完成！"
```

### 5.4 成本与时间对比
```
案例：电商双 11 活动 (50 个产品 × 3 个版本 × 4 个平台 = 600 个视频)

传统方案:
- 拍摄：50 产品 × ¥2000 = ¥100,000
- 剪辑：600 视频 × ¥200 = ¥120,000
- 周期：4-6 周
- 总成本：¥220,000+
- 修改成本：¥50,000+ (每次)

AI + Remotion 方案:
- AI 视频生成：50 产品 × ¥50 = ¥2,500
- Remotion 模板开发：¥10,000 (一次性)
- 批量渲染：¥0 (本地)
- 周期：1 周
- 总成本：¥12,500 (首单) / ¥2,500 (复购)
- 修改成本：¥0 (改代码重渲染)

ROI:
- 成本节省：94%+
- 时间节省：75%+
- 迭代速度：10 倍+
```

---

## 六、最佳实践与技巧 (8min)

### 6.1 性能优化
```tsx
// 1. 使用 useMemo 避免重复计算
const ExpensiveComponent = ({ data }) => {
  const processed = useMemo(() => {
    // 耗时操作
    return heavyComputation(data);
  }, [data]);
  
  return <div>{processed}</div>;
};

// 2. 延迟加载大文件
const LazyVideo = lazy(() => import('./VideoComponent'));

// 3. 缓存 AI 素材
const AssetCache = new Map();
const getCachedAsset = async (url) => {
  if (AssetCache.has(url)) return AssetCache.get(url);
  const asset = await downloadAsset(url);
  AssetCache.set(url, asset);
  return asset;
};
```

### 6.2 调试技巧
```bash
# 1. 单帧预览
npx remotion preview --frame=150

# 2. 导出调试信息
npx remotion render --log=verbose

# 3. 使用 Remotion DevTools
# 在 browser 中打开开发者工具

# 4. 性能分析
npx remotion benchmark
```

### 6.3 常见陷阱与解决
```
问题 1: 视频渲染出来是黑屏
解决：检查所有媒体路径，确保是绝对路径或正确相对路径

问题 2: 动画卡顿
解决：降低分辨率测试，检查是否有性能瓶颈组件

问题 3: 音频不同步
解决：检查 FPS 设置，确保所有素材 FPS 一致

问题 4: 字体不显示
解决：在服务器上安装所需字体，或使用 Web Font
```

---

## 七、延伸：与分镜 Agent 集成 (5min)

```python
# 分镜 Agent 输出 Remotion 配置
class RemotionConfigGenerator:
    def generate_config(self, storyboard: Storyboard) -> dict:
        """从分镜生成 Remotion 配置"""
        config = {
            "composition": {
                "durationInFrames": storyboard.total_duration * 30,
                "fps": 30,
                "width": 1080,
                "height": 1920,
            },
            "sequences": []
        }
        
        for scene in storyboard.scenes:
            for shot in scene.shots:
                sequence = {
                    "from": shot.start_frame,
                    "durationInFrames": shot.duration * 30,
                    "component": self._map_shot_to_component(shot),
                    "props": {
                        "video": shot.ai_video_url,
                        "transition": shot.transition_type,
                    }
                }
                config["sequences"].append(sequence)
        
        return config
    
    def export_tsx(self, config: dict) -> str:
        """导出为 TypeScript 代码"""
        # 生成 Remotion 组件代码
        return tsx_code

# 工作流整合
storyboard = storyboard_agent.generate(script)
remotion_config = generator.generate_config(storyboard)
generator.export_tsx(remotion_config)
# 自动渲染
subprocess.run(["npm", "run", "build"])
```

---

## 八、实操练习 (5min)

### 练习 1: 基础模板
- 搭建 Remotion 环境
- 创建第一个可配置广告模板
- 渲染输出 MP4

### 练习 2: AI 素材集成
- 用 Runway/Kling 生成产品视频
- 用 Suno 生成背景音乐
- 集成到 Remotion 模板

### 练习 3: 批量生成
- 准备 5 个产品配置
- 批量渲染 5 个变体
- 输出到不同平台尺寸

### 练习 4: A/B 测试
- 设计 3 个不同开场
- 生成所有组合变体
- 部署测试

---

## 九、思考题

1. 可编辑视频工作流的核心价值是什么？
2. Remotion 与传统视频编辑软件的本质区别？
3. AI 生成 + 可编程合成的边界在哪里？
4. 如何设计一个支持多人协作的 Remotion 模板系统？
