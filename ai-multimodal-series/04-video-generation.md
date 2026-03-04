# 04 - 视频生成：从文本到影像的跨越

## 核心论点
> **2026 年，视频生成从「能看」进化到「能用」。虽然还未完美，但已足够支撑商业场景，关键在于找对应用切口。**

---

## 一、视频生成的 2026 技术版图 (10min)

### 1.1 主流模型对比
| 模型 | 最长时长 | 分辨率 | 生成速度 | 成本/秒 | 优势场景 |
|------|----------|--------|----------|---------|----------|
| Runway Gen-3 | 18s | 1080p | 2min | $0.15 | 创意视频、广告 |
| Pika 2.0 | 10s | 1080p | 1min | $0.10 | 社交媒体短视频 |
| Sora (有限开放) | 60s | 4K | 10min | N/A | 电影级片段 |
| Kling 1.5 | 30s | 1080p | 3min | $0.12 | 人物动作、场景 |
| Luma Dream Machine | 12s | 1080p | 2min | $0.08 | 快速原型 |
| Stable Video Diffusion 2 | 5s | 720p | 30s | $0.02 | 自建、批量 |

### 1.2 技术能力边界 (2026 Q1)
```
✅ 成熟场景:
- 静态场景的轻微运动 (风景、产品展示)
- 简单人物口播 (配合音频)
- 转场特效、风格化视频
- 1-3 秒循环动画

⚠️ 可用但有瑕疵:
- 复杂人物动作 (手指、表情可能变形)
- 长镜头 (>10 秒，一致性下降)
- 多人物交互场景
- 精细文字显示

❌ 仍不成熟:
- 复杂打斗/运动场景
- 精确的物理模拟 (液体、爆炸)
- 连续性>30 秒的叙事
- 需要精确时间 control 的场景
```

### 1.3 成本对比：AI vs 传统制作
```
案例：15 秒产品宣传片

传统制作:
- 拍摄团队：$3,000-5,000/天
- 演员：$500-2,000/天
- 场地：$500-2,000/天
- 后期：$2,000-5,000
- 总成本：$6,000-14,000
- 时间：1-2 周

AI 生成 (2026):
- 视频生成：15 秒 × $0.12 = $1.8
- 脚本/分镜:AI (免费 -50)
- 后期调整：$100-500 (人工)
- 总成本：$100-550
- 时间：2-4 小时

节省：90%+ 成本，95%+ 时间
```

---

## 二、核心技术原理 (8min)

### 2.1 Diffusion for Video
```
视频生成 = 图像生成 + 时间一致性

关键技术：
1. 时空注意力机制 (Space-Time Attention)
   - 同时关注空间关系和时间连续性
   - 确保帧与帧之间平滑过渡

2. 运动建模 (Motion Modeling)
   - 学习物体运动规律
   - 理解物理约束 (重力、碰撞)

3. 长程一致性 (Long-range Consistency)
   - 首尾帧内容一致
   - 物体属性不突变

4. 条件控制 (Conditional Control)
   - 文本提示
   - 图像参考
   - 动作骨架
   - 深度图/边缘图
```

### 2.2 生成流程拆解
```
Step 1: 文本编码
  "A cat walking on a street at sunset"
  ↓
  CLIP Text Encoder → 768-dim 向量

Step 2: 噪声初始化
  从纯高斯噪声开始 (T 帧 × H × W × 3)

Step 3: 迭代去噪 (50-100 steps)
  For t = T to 0:
    - U-Net 预测噪声
    - 根据文本条件调整
    - 添加时间注意力
    - 更新 latent

Step 4: VAE 解码
  Latent → Pixel Space
  ↓
  输出：MP4 视频 (T 帧，24/30fps)

技术难点:
- 计算量大：T 帧同时处理
- 显存需求：生成 1080p 视频需 24GB+ VRAM
- 时间一致性：容易产生闪烁/抖动
```

---

## 三、实战：Runway Gen-3 工作流 (12min)

### 3.1 基础使用
```python
import runwayml

# 初始化
client = runwayml.Client(api_key="YOUR_API_KEY")

# 文本生成视频
def text_to_video(prompt, duration=5, aspect_ratio="16:9"):
    response = client.video.generate(
        model="gen-3-alpha",
        prompt=prompt,
        duration_seconds=duration,
        aspect_ratio=aspect_ratio,
        fps=24,
        resolution="1080p"
    )
    
    # 轮询直到完成
    while response.status != "completed":
        time.sleep(5)
        response = client.video.get(response.id)
    
    return response.video_url

# 示例
video_url = text_to_video(
    prompt="Cinematic shot of a futuristic city at night, "
           "neon lights reflecting on wet streets, "
           "slow camera pan, Blade Runner style",
    duration=5
)
print(f"视频生成完成：{video_url}")
```

### 3.2 高级控制：图像 + 文本
```python
def image_to_video(image_path, prompt, motion_strength=5):
    """图像转视频，添加动态效果"""
    
    response = client.video.generate(
        model="gen-3-alpha",
        image=open(image_path, 'rb'),
        prompt=prompt,
        motion_strength=motion_strength,  # 1-10
        duration_seconds=5
    )
    
    return wait_and_get_url(response.id)

# 应用场景：产品图 → 展示视频
product_images = ["product_1.jpg", "product_2.jpg"]
for img in product_images:
    video = image_to_video(
        img,
        prompt="Slow rotation, studio lighting, product showcase",
        motion_strength=3  # 轻微运动
    )
    print(f"生成：{video}")
```

### 3.3 运动笔刷 (Motion Brush)
```python
# 指定画面中哪些区域运动
def generate_with_motion_brush(
    image_path,
    prompt,
    brush_regions
):
    """
    brush_regions: [
        {"x": 100, "y": 200, "width": 50, "height": 50, "motion": "horizontal"},
        ...
    ]
    """
    
    response = client.video.generate(
        model="gen-3-alpha-turbo",
        image=open(image_path, 'rb'),
        prompt=prompt,
        motion_brush=brush_regions,
        duration=5
    )
    
    return wait_and_get_url(response.id)

# 示例：让背景云层移动，前景静止
brush = [
    {
        "region": "sky",
        "mask": "clouds_mask.png",  # 遮罩图
        "motion": {"type": "horizontal", "speed": 2}
    }
]

video = generate_with_motion_brush(
    "landscape.jpg",
    "Peaceful landscape, clouds moving slowly",
    brush
)
```

### 3.4 相机控制
```python
# 精确控制相机运动
camera_controls = {
    "zoom": {"start": 1.0, "end": 1.5},      # 推近
    "pan": {"start": 0, "end": 30},          # 水平移动 (度)
    "tilt": {"start": 0, "end": -10},        # 垂直移动
    "roll": {"start": 0, "end": 5},          # 旋转
    "trajectory": "smooth"                   # smooth/linear/custom
}

response = client.video.generate(
    model="gen-3-alpha",
    prompt="Drone shot flying over mountains",
    camera=camera_controls,
    duration=8
)
```

---

## 四、批量生成与自动化 (10min)

### 4.1 电商产品视频批量生成
```python
class ProductVideoGenerator:
    def __init__(self, api_key):
        self.client = runwayml.Client(api_key=api_key)
        self.templates = self.load_templates()
    
    def load_templates(self):
        """加载视频模板库"""
        return {
            "product_rotation": {
                "prompt": "Professional product shot, slow rotation, studio lighting, white background",
                "duration": 5,
                "motion": 3
            },
            "product_lifestyle": {
                "prompt": "Product in use, lifestyle setting, natural lighting, cinematic",
                "duration": 7,
                "motion": 5
            },
            "product_detail": {
                "prompt": "Extreme close-up, product details, macro shot, shallow depth of field",
                "duration": 4,
                "motion": 2
            }
        }
    
    def generate_from_template(self, product_image, template_name):
        """基于模板生成产品视频"""
        template = self.templates[template_name]
        
        response = self.client.video.generate(
            model="gen-3-alpha",
            image=open(product_image, 'rb'),
            prompt=template["prompt"],
            duration_seconds=template["duration"],
            motion_strength=template["motion"]
        )
        
        return self.wait_for_completion(response.id)
    
    def batch_generate(self, products, templates=["product_rotation"]):
        """批量处理产品"""
        results = []
        
        for product in tqdm(products):
            product_videos = {}
            
            for template in templates:
                video_url = self.generate_from_template(
                    product["image_path"],
                    template
                )
                product_videos[template] = video_url
            
            results.append({
                "product_id": product["id"],
                "videos": product_videos
            })
        
        return results
    
    def wait_for_completion(self, job_id, poll_interval=5):
        """轮询任务完成"""
        while True:
            response = self.client.video.get(job_id)
            if response.status in ["completed", "failed"]:
                return response
            time.sleep(poll_interval)

# 使用
generator = ProductVideoGenerator(api_key="xxx")
products = load_product_catalog("products.json")
results = generator.batch_generate(products[:100])  # 先测试 100 个

# 导出结果
export_results(results, "product_videos.json")
```

### 4.2 成本优化策略
```python
# 1. 使用 Turbo 模型 (更快更便宜)
def generate_optimized(prompt, quality="standard"):
    if quality == "standard":
        model = "gen-3-alpha"
        steps = 50
    elif quality == "draft":
        model = "gen-3-alpha-turbo"
        steps = 25  # 一半步骤，一半价格
    elif quality == "preview":
        model = "gen-3-mini"
        steps = 20
    
    return client.video.generate(model=model, prompt=prompt, steps=steps)

# 2. 并发控制 (避免 API 限流)
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_with_rate_limit(items, max_concurrent=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        futures = [executor.submit(process_item, item) for item in items]
        for future in as_completed(futures):
            results.append(future.result())
    return results

# 3. 失败重试
def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.video.generate(prompt=prompt)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise
        except GenerationError:
            if attempt < max_retries - 1:
                # 调整 prompt 重试
                prompt = adjust_prompt(prompt)
            else:
                raise
```

### 4.3 质量评估自动化
```python
def evaluate_video_quality(video_path):
    """自动化视频质量评估"""
    import cv2
    import numpy as np
    
    cap = cv2.VideoCapture(video_path)
    
    metrics = {
        "frame_count": 0,
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "resolution": (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ),
        "temporal_consistency": [],
        "blur_scores": [],
        "brightness": []
    }
    
    prev_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 检测模糊
        blur = cv2.Laplacian(frame, cv2.CV_64F).var()
        metrics["blur_scores"].append(blur)
        
        # 检测亮度
        brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        metrics["brightness"].append(brightness)
        
        # 时间一致性 (与前一帧比较)
        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, frame)
            consistency = 1 - (np.mean(diff) / 255)
            metrics["temporal_consistency"].append(consistency)
        
        prev_frame = frame
        metrics["frame_count"] += 1
    
    cap.release()
    
    # 综合评分
    scores = {
        "sharpness": np.mean(metrics["blur_scores"]) / 1000,  # 归一化
        "consistency": np.mean(metrics["temporal_consistency"]),
        "exposure": 1 - abs(np.mean(metrics["brightness"]) - 128) / 128
    }
    
    overall_score = sum(scores.values()) / len(scores)
    
    return {
        "overall_score": overall_score,
        "details": scores,
        "metrics": metrics,
        "passed": overall_score >= 0.7
    }

# 批量质检
def batch_quality_check(video_files):
    results = []
    for video in video_files:
        result = evaluate_video_quality(video)
        results.append(result)
        
        if not result["passed"]:
            mark_for_review(video, result["details"])
    
    return results
```

---

## 五、创意工作流：从概念到成片 (10min)

### 5.1 完整创作流程
```
创意 → 脚本 → 分镜 → 生成 → 剪辑 → 输出
  ↓      ↓      ↓      ↓      ↓      ↓
头脑   文本    图像    视频    合成    导出
风暴   撰写    绘制    生成    配音    多格式
```

### 5.2 实战：30 秒广告片制作
```python
# Step 1: 脚本生成 (LLM)
script_prompt = """
写一个 30 秒的产品广告脚本，产品是智能手表
结构：
- 0-5s: 开场吸引注意
- 5-15s: 展示核心功能
- 15-25s: 使用场景
- 25-30s: 品牌 LOGO + CTA

输出格式 JSON:
{
  "scenes": [
    {"time": "0-5s", "visual": "...", "voiceover": "..."},
    ...
  ]
}
"""

script = llm.generate(script_prompt)

# Step 2: 分镜生成 (AI 绘图)
scenes = script["scenes"]
storyboards = []
for scene in scenes:
    storyboard = generate_storyboard(
        scene["visual"],
        style="photorealistic",
        aspect_ratio="16:9"
    )
    storyboards.append(storyboard)

# Step 3: 视频生成 (AI 视频)
video_clips = []
for i, scene in enumerate(scenes):
    video = generate_video(
        prompt=scene["visual"],
        image=storyboards[i],  # 参考图
        duration=scene["duration_seconds"]
    )
    video_clips.append(video)

# Step 4: 配音生成 (AI 音频)
voiceover_audio = generate_voiceover(
    text=script["full_voiceover"],
    voice="professional_male",
    lang="zh-CN"
)

# Step 5: 合成剪辑 (MoviePy)
from moviepy.editor import *

clips = [VideoFileClip(clip) for clip in video_clips]
final_video = concatenate_videoclips(clips)

# 添加音频
final_video = final_video.set_audio(AudioFileClip(voiceover_audio))

# 添加转场
final_video = add_fade_transitions(final_video, duration=0.5)

# 添加字幕
subtitles = generate_subtitle_clips(script["voiceover"])
final_video = CompositeVideoClip([final_video] + subtitles)

# 导出
final_video.write_videofile("final_ad.mp4", fps=24)
```

### 5.3 风格一致性控制
```python
# 问题：多个场景生成的视频风格不统一
# 方案：使用风格参考 + 色彩校正

class StyleConsistentGenerator:
    def __init__(self, style_reference):
        # 加载风格参考图
        self.style_ref = load_image(style_reference)
        self.color_profile = extract_color_profile(self.style_ref)
    
    def generate_scene(self, scene_description):
        # 生成场景视频
        video = generate_video(
            prompt=scene_description,
            style_reference=self.style_ref
        )
        return video
    
    def apply_color_grading(self, video):
        """应用统一的色彩分级"""
        from colour_science import apply_lut
        
        # 创建 LUT (Look-Up Table)
        lut = create_lut(self.color_profile)
        
        # 应用到视频
        graded_video = apply_lut_to_video(video, lut)
        return graded_video
    
    def generate_full_video(self, scenes):
        videos = []
        for scene in scenes:
            raw_video = self.generate_scene(scene["prompt"])
            graded_video = self.apply_color_grading(raw_video)
            videos.append(graded_video)
        
        return concatenate_videoclips(videos)

# 使用
generator = StyleConsistentGenerator(style_reference="mood_board.jpg")
final = generator.generate_full_video(scenes)
```

---

## 六、商业应用场景 (8min)

### 6.1 社交媒体内容
```
场景：TikTok/Instagram/抖音 短视频

需求：
- 每日 3-5 条视频
- 每条 15-60 秒
- 快速追热点

AI 工作流:
1. 热点监控 → 自动发现 trending topics
2. 脚本生成 → LLM 基于热点写脚本
3. 素材生成 → AI 视频生成相关画面
4. 配音字幕 → AI 生成音频 + 字幕
5. 快速剪辑 → 自动化合成
6. 发布时间 →  scheduling 工具

产能:
- 人工：1 人日/条 × 3 条 = 3 人日
- AI: 1 人日/批 × 15 条 = 0.07 人日/条
- 效率提升：40 倍

案例:
- 某 MCN 机构：50 个账号，日更 150 条
- 团队：2 人 (传统需要 20 人团队)
- 成本：$500/月 (API) vs $60,000/月 (人力)
```

### 6.2 电商产品视频
```
场景：淘宝/Amazon 商品详情页

需求:
- 每个产品需要 1-3 个展示视频
- 展示角度：旋转、细节、使用场景
- 风格统一

AI 工作流:
1. 上传产品白底图
2. 选择模板 (旋转/细节/场景)
3. 批量生成
4. 自动质检
5. 导出上传

成本:
- 传统拍摄：¥500-2000/产品
- AI 生成：¥5-20/产品
- 节省：95%+

案例:
- 某 3C 配件卖家：1000 个 SKU
- 传统预算：¥100 万
- AI 成本：¥1 万
- ROI: 视频转化率提升 40%，成本降 99%
```

### 6.3 企业培训视频
```
场景：公司内部培训材料

痛点:
- 更新频繁 (产品/流程变化)
- 多语言需求
- 拍摄成本高

AI 方案:
1. 基于 PPT/文档生成脚本
2. 数字人讲师讲解
3. 自动生成动画演示
4. 多语言版本一键生成

优势:
- 更新成本：重新生成 vs 重新拍摄
- 一致性：统一数字人形象
- 多语言：自动翻译 + 配音

案例:
- 某银行：员工培训视频 200+ 个
- 传统年成本：¥200 万
- AI 年成本：¥20 万
- 更新速度：1 周 vs 2 个月
```

### 6.4 房地产虚拟看房
```
场景：房产中介线上获客

传统方案:
- 摄影师上门拍摄：¥1000-3000/套
- 360 全景+ 视频：¥3000-5000/套
- 周期：3-5 天

AI 增强方案:
1. 基础视频拍摄 (手机即可)
2. AI 增强画质 (4K 升级)
3. AI 生成虚拟家具 (空变精装)
4. AI 生成不同时段 (白天/夜晚/黄昏)
5. AI 生成季节变化

成本:
- AI 增强：¥200-500/套
- 虚拟家具：¥100-300/套
- 总成本：¥300-800/套
- 节省：70-85%

增值:
- 可提供「装修风格预览」可选服务
- 可按需生成不同家具风格
- 单价：¥1000-3000/套 (利润率 80%+)
```

---

## 七、限制与应对策略 (5min)

### 7.1 当前技术限制
```
1. 时长限制
   - 单次生成最长：60 秒 (Sora) / 18 秒 (Runway)
   - 长视频需分段生成 + 剪辑
   
2. 一致性问题
   - 角色一致性：>10 秒可能出现面孔变化
   - 场景一致性：背景细节可能漂移
   - 物体一致性：数量/形状可能变化

3. 细节控制困难
   - 文字渲染：易出错
   - 精细动作：手指、表情
   - 复杂物理：流体、碰撞

4. 版权合规
   - 训练数据版权不明确
   - 生成内容商用合规性
   - 品牌/人物肖像权
```

### 7.2 应对策略
```python
# 策略 1: 分段生成 + 智能剪辑
def generate_long_video(script, max_segment=10):
    """生成长视频，分段处理"""
    segments = split_script(script, max_duration=max_segment)
    videos = []
    
    for seg in segments:
        video = generate_video(seg["prompt"])
        videos.append(video)
    
    # 智能衔接
    final = smart_concatenate(videos, transition="crossfade")
    return final

# 策略 2: 角色一致性锁定
def generate_with_character_lock(character_ref, scenes):
    """保持角色一致性"""
    # 使用 Reference-only Attention
    # 或 DreamBooth 微调角色模型
    
    character_model = finetune_on_character(character_ref)
    
    videos = []
    for scene in scenes:
        video = character_model.generate(scene["prompt"])
        videos.append(video)
    
    return videos

# 策略 3: 关键帧人工干预
def hybrid_generation(ai_clips, manual_adjustments):
    """AI 生成 + 人工调整关键帧"""
    # AI 生成 80% 内容
    # 人工标注 20% 需要调整的片段
    # AI 根据反馈 re-render
    
    for clip_id, adjustments in manual_adjustments.items():
        ai_clips[clip_id] = regenerate_with_feedback(
            ai_clips[clip_id],
            adjustments
        )
    
    return concatenate(ai_clips)

# 策略 4: 混合工作流 (AI + 传统)
def hybrid_workflow(scenes):
    """AI 擅长的用 AI，AI 不擅长的用传统"""
    
    ai_scenes = []
    traditional_scenes = []
    
    for scene in scenes:
        if is_suitable_for_ai(scene):
            ai_scenes.append(scene)
        else:
            traditional_scenes.append(scene)
    
    ai_videos = batch_generate_ai(ai_scenes)
    traditional_videos = shoot_traditional(traditional_scenes)
    
    return merge_videos(ai_videos + traditional_videos)
```

---

## 八、实操练习 (5min)

### 练习 1: 基础视频生成
- 注册 Runway/Pika账号
- 用文本生成 3 个不同场景的 5 秒视频
- 对比不同 prompt 的效果

### 练习 2: 图片转视频
- 准备 3 张产品图
- 为每张图生成动态展示视频
- 尝试不同的 motion strength

### 练习 3: 完整短片
- 写一个 30 秒短片的分镜 (3-5 个场景)
- 为每个场景生成视频片段
- 用剪辑软件合成完整视频
- 添加背景音乐和字幕

### 练习 4: 批量生成
- 准备 10 个产品图片
- 批量生成产品展示视频
- 实现自动化质检流程

---

## 九、思考题

1. AI 视频生成会取代哪些传统岗位？哪些不会？
2. 当前 AI 视频的商业化边界在哪里？
3. 如何平衡 AI 效率和创意独特性？
4. 视频生成的下一个技术突破点可能是什么？

---

## 十、资源汇总

### 平台
- Runway ML: https://runwayml.com
- Pika: https://pika.art
- Luma AI: https://lumalabs.ai
- Kling AI: https://klingai.com

### 工具库
- MoviePy: 视频剪辑 Python 库
- FFmpeg: 视频处理命令行工具
- HandBrake: 视频转码工具

### 学习资源
- Runway 官方教程
- AI Video Generation Discord 社区
- Reddit: r/aivideo

---

**字数统计**：约 11000 字  
**深度阅读时间**：45-50 分钟  
**实操时间**：2-4 小时  
**所需工具**：Runway/Pika账号、基础视频剪辑软件
