# 06 - 视频生成结合分镜 Agent 生成短剧

## 核心论点
> **短剧市场 2026 年爆发至 500 亿规模，但制作成本仍是瓶颈。分镜 Agent 工作流将单集成本从¥5 万降至¥5 千，让「一人剧组」成为可能。**

---

## 一、短剧市场与 AI 机会 (10min)

### 1.1 市场规模与痛点
```
中国 short drama 市场数据 (2026):
- 市场规模：¥500 亿/年 (2023 年¥300 亿 → 2026 年¥500 亿)
- 日活跃用户：1.2 亿
- 付费用户：8000 万
- 平均单部成本：¥30-100 万 (传统)
- 平均回本周期：2-4 周
- 成功率：约 10-15%

核心痛点:
1. 成本高：演员 + 场地 + 设备 + 后期 = ¥50 万/部起步
2. 周期长：剧本→拍摄→剪辑 = 4-8 周
3. 风险大：90% 项目亏损，但失败成本照付
4. 人力密集：需要完整剧组 (10-30 人)
5. 无法快速迭代：拍完发现不行，沉没成本已发生

AI 机会:
- 成本降低：90%+ (¥50 万 → ¥5 万)
- 周期缩短：80%+ (6 周 → 1 周)
- 风险降低：先验证后投入
- 人力减少：1 人可完成 10 人工作
```

### 1.2 传统短剧制作流程
```
阶段 1: 前期筹备 (1-2 周)
  - 剧本创作 (编剧 2-3 人)
  - 分镜设计 (分镜师)
  - 选角 casting (导演 + 制片)
  - 场地勘景 (美术 + 制片)
  - 预算：¥5-10 万 (失败则全损)

阶段 2: 拍摄 (3-7 天)
  - 演员：3-5 个主要角色
  - 剧组:10-20 人 (摄影、灯光、收音、场务...)
  - 设备：摄影机、灯光、轨道...
  - 日成本：¥3-8 万/天
  - 预算：¥15-40 万

阶段 3: 后期制作 (1-2 周)
  - 剪辑：¥1-3 万
  - 调色：¥1-2 万
  - 音效/配乐:¥1-3 万
  - 特效：¥2-10 万 (如有)
  - 预算：¥5-18 万

总计：¥25-68 万/部 (80-100 集，每集 1-2 分钟)
时间：6-11 周
人力：15-25 人
```

### 1.3 AI 工作流对比
```
阶段 1: 前期 AI 化 (1-2 天)
  - 剧本创作：LLM 辅助 (0.5 天)
  - 分镜生成：AI 绘图 + 分镜 Agent (0.5 天)
  - 角色设计:AI 绘图 + 数字人创建 (0.5 天)
  - 场景设计：AI 生成参考图 (0.5 天)
  - 预算：¥200-500 (API 成本)

阶段 2: 视频生成 (2-4 天)
  - 场景视频：AI 视频生成 (Runway/Kling)
  - 角色表演：数字人驱动 (HeyGen/D-ID)
  - 动作镜头:AI 视频 + 后期合成
  - 预算：¥2000-5000 (API 成本)

阶段 3: 后期 AI 化 (1-2 天)
  - 剪辑：自动化 + 人工精修
  - 调色:AI 自动调色
  - 音效/配乐:AI 生成 (Suno/Udio)
  - 字幕：自动生成
  - 预算：¥500-1000 (API 成本)

总计：¥3000-7000/部
时间：4-8 天
人力：1-2 人
节省：成本 90%+,时间 70%+,人力 90%+
```

---

## 二、分镜 Agent 系统设计 (15min)

### 2.1 系统架构
```
┌─────────────────────────────────────────────────────┐
│                  分镜 Agent 系统                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐    ┌──────────────┐               │
│  │  剧本输入     │    │  风格参考     │               │
│  │  (.md/.txt)  │    │  (图片/视频)  │               │
│  └──────┬───────┘    └──────┬───────┘               │
│         │                    │                       │
│         └────────┬───────────┘                       │
│                  ↓                                    │
│  ┌──────────────────────────────────────┐            │
│  │        Scene Understanding Agent     │            │
│  │  - 场景分析 (时间、地点、氛围)          │            │
│  │  - 角色识别 (谁在场、情绪状态)          │            │
│  │  - 动作分解 (关键动作、镜头需求)        │            │
│  │  - 对话标注 (谁说什么、语气)            │            │
│  └────────────────┬─────────────────────┘            │
│                   ↓                                   │
│  ┌──────────────────────────────────────┐            │
│  │        Storyboard Generation Agent   │            │
│  │  - 分镜草图生成 (AI 绘图)              │            │
│  │  - 镜头语言设计 (景别、角度、运动)      │            │
│  │  - 转场设计 (场景切换方式)              │            │
│  │  - 时长估算 (每镜几秒)                  │            │
│  └────────────────┬─────────────────────┘            │
│                   ↓                                   │
│  ┌──────────────────────────────────────┐            │
│  │        Video Generation Agent        │            │
│  │  - 场景视频生成 (Runway/Kling)        │            │
│  │  - 角色视频生成 (数字人驱动)           │            │
│  │  - 镜头拼接与转场                     │            │
│  │  - 质量检查 (一致性、流畅度)           │            │
│  └────────────────┬─────────────────────┘            │
│                   ↓                                   │
│  ┌──────────────────────────────────────┐            │
│  │        Post-Production Agent         │            │
│  │  - 自动剪辑 (按分镜组装)              │            │
│  │  - AI 配乐生成 (Suno)                 │            │
│  │  - 音效添加 (AI 音效库)               │            │
│  │  - 字幕生成 (语音识别)                │            │
│  │  - 调色统一 (风格化)                  │            │
│  └────────────────┬─────────────────────┘            │
│                   ↓                                   │
│              成品视频输出                              │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 2.2 剧本解析 Agent
```python
from pydantic import BaseModel, Field
from typing import List, Optional
import llm

class Character(BaseModel):
    name: str
    age_range: str
    gender: str
    description: str
    emotion: str

class Scene(BaseModel):
    scene_number: int
    location: str
    time_of_day: str
    atmosphere: str
    characters: List[Character]
    actions: List[str]
    dialogues: List[dict]  # {"speaker": str, "text": str, "tone": str}
    camera_shots: List[str]
    estimated_duration: int  # seconds

class ScriptAnalysis(BaseModel):
    title: str
    genre: str
    total_scenes: int
    total_duration: int
    main_characters: List[Character]
    scenes: List[Scene]
    visual_style: str
    reference_works: List[str]

class ScriptAnalyzer:
    def __init__(self, model="gpt-4"):
        self.llm = LLMClient(model=model)
    
    def analyze(self, script_text: str) -> ScriptAnalysis:
        """解析剧本"""
        prompt = f"""
        分析以下短剧剧本，输出结构化 JSON 格式：

        要求:
        1. 识别所有场景 (scene)
        2. 提取每个场景的要素:
           - 地点 (location): 室内/室外，具体位置
           - 时间 (time_of_day): 白天/夜晚/黄昏/黎明
           - 氛围 (atmosphere): 温馨/紧张/悬疑/浪漫等
           - 角色 (characters): 在场人物及情绪状态
           - 动作 (actions): 关键动作描述
           - 对话 (dialogues): 谁说什么，语气如何
           - 镜头建议 (camera_shots): 特写/中景/全景，推/拉/摇/移
           - 时长估算 (duration): 这个场景预计几秒

        3. 总结视觉风格建议
        4. 推荐参考作品 (类似风格的影视)

        输出格式：严格的 JSON，符合 ScriptAnalysis schema

        剧本内容:
        {script_text[:8000]}  # 截取前 8000 字符
        """
        
        response = self.llm.generate(prompt, response_format=ScriptAnalysis)
        return ScriptAnalysis(**response)
    
    def extract_visual_prompts(self, scene: Scene) -> List[dict]:
        """为每个场景生成视频生成 prompt"""
        prompts = []
        
        for shot in scene.camera_shots:
            # 构建详细的视觉 prompt
            visual_prompt = {
                "shot_type": shot,
                "prompt": self._build_shot_prompt(scene, shot),
                "negative_prompt": "deformed, blurry, low quality, distorted faces",
                "duration": min(5, scene.estimated_duration),
                "aspect_ratio": "9:16"  # 竖屏短剧
            }
            prompts.append(visual_prompt)
        
        return prompts
    
    def _build_shot_prompt(self, scene: Scene, shot_type: str) -> str:
        """构建单个镜头的 prompt"""
        base = f"{scene.location}, {scene.time_of_day}, {scene.atmosphere} atmosphere"
        
        characters_desc = ", ".join([
            f"{c.name}, {c.gender}, {c.age_range}, {c.emotion} expression"
            for c in scene.characters
        ])
        
        actions_desc = ", ".join(scene.actions[:3])  # 最多 3 个动作
        
        shot_mapping = {
            "特写": "extreme close-up, detailed facial expression",
            "中景": "medium shot, waist-up framing",
            "全景": "full body shot, wide angle",
            "过肩镜头": "over-the-shoulder shot",
            "俯拍": "high angle shot, looking down",
            "仰拍": "low angle shot, looking up",
            "推镜头": "slow push in, increasing tension",
            "拉镜头": "slow pull out, revealing context"
        }
        
        shot_desc = shot_mapping.get(shot_type, shot_type)
        
        return f"{shot_desc}, {base}, {characters_desc}, {actions_desc}, cinematic lighting, high quality, dramatic"
```

### 2.3 分镜生成 Agent
```python
class StoryboardAgent:
    def __init__(self):
        self.image_gen = ImageGenerator()  # Nano Banana 2 / Midjourney
        self.script_analyzer = ScriptAnalyzer()
    
    def generate_storyboard(self, script_path: str, style_reference: str = None):
        """生成完整分镜"""
        # 1. 解析剧本
        with open(script_path, 'r', encoding='utf-8') as f:
            script_text = f.read()
        
        analysis = self.script_analyzer.analyze(script_text)
        
        # 2. 为每个场景生成分镜图
        storyboards = []
        for scene in analysis.scenes:
            scene_boards = self._generate_scene_storyboard(scene, style_reference)
            storyboards.append({
                "scene": scene,
                "storyboards": scene_boards
            })
        
        # 3. 导出分镜文档
        self._export_storyboard_doc(storyboards, analysis)
        
        return storyboards
    
    def _generate_scene_storyboard(self, scene: Scene, style_ref: str) -> List[dict]:
        """为单个场景生成多个分镜"""
        prompts = self.script_analyzer.extract_visual_prompts(scene)
        boards = []
        
        for i, prompt in enumerate(prompts):
            # 生成预览图
            image = self.image_gen.generate(
                prompt=prompt["prompt"],
                negative_prompt=prompt["negative_prompt"],
                style_reference=style_ref,
                aspect_ratio="9:16"
            )
            
            boards.append({
                "shot_index": i,
                "shot_type": prompt["shot_type"],
                "image": image,
                "prompt": prompt["prompt"],
                "duration": prompt["duration"],
                "description": f"场景{scene.scene_number}-{i+1}: {prompt['shot_type']}"
            })
        
        return boards
    
    def _export_storyboard_doc(self, storyboards, analysis):
        """导出分镜文档 (Markdown + 图片)"""
        doc = f"# {analysis.title} - 分镜脚本\n\n"
        doc += f"**类型**: {analysis.genre}\n"
        doc += f"**总时长**: {analysis.total_duration}秒\n"
        doc += f"**总场景数**: {analysis.total_scenes}\n\n"
        doc += f"**视觉风格**: {analysis.visual_style}\n\n"
        doc += f"**参考作品**: {', '.join(analysis.reference_works)}\n\n"
        doc += "---\n\n"
        
        for sb in storyboards:
            scene = sb["scene"]
            doc += f"## 场景 {scene.scene_number}: {scene.location}\n\n"
            doc += f"**时间**: {scene.time_of_day} | **氛围**: {scene.atmosphere}\n\n"
            doc += f"**在场角色**: {', '.join([c.name for c in scene.characters])}\n\n"
            
            for i, board in enumerate(sb["storyboards"]):
                doc += f"### 镜头 {i+1}: {board['shot_type']}\n"
                doc += f"**时长**: {board['duration']}秒\n"
                doc += f"**描述**: {board['description']}\n"
                doc += f"**Prompt**: `{board['prompt']}`\n"
                doc += f"![分镜图]({board['image']})\n\n"
            
            doc += "---\n\n"
        
        with open("storyboard.md", 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"✅ 分镜文档已生成：storyboard.md")
```

### 2.4 视频生成 Agent
```python
class VideoGenerationAgent:
    def __init__(self):
        self.runway_client = RunwayClient()
        self.kling_client = KlingClient()
        self.heygen_client = HeyGenClient()
    
    def generate_scene_videos(self, storyboards: List[dict]) -> List[str]:
        """为所有分镜生成视频片段"""
        video_clips = []
        
        for sb in storyboards:
            scene_clips = []
            for board in sb["storyboards"]:
                # 判断是否需要数字人
                if self._needs_digital_human(board):
                    # 数字人表演
                    clip = self._generate_digital_human_clip(board)
                else:
                    # 场景视频
                    clip = self._generate_scene_clip(board)
                
                scene_clips.append(clip)
            
            video_clips.append(scene_clips)
        
        return video_clips
    
    def _needs_digital_human(self, board: dict) -> bool:
        """判断是否需要数字人"""
        # 检测 prompt 中是否有人物对话/特写
        prompt = board["prompt"].lower()
        keywords = ["talking", "speaking", "dialogue", "close-up", "face"]
        return any(kw in prompt for kw in keywords)
    
    def _generate_digital_human_clip(self, board: dict) -> str:
        """生成数字人表演片段"""
        # 提取对话内容
        dialogue = self._extract_dialogue(board)
        
        # 生成数字人视频
        video = self.heygen_client.generate(
            script=dialogue["text"],
            avatar_id=self._select_avatar(dialogue["speaker"]),
            voice=self._get_voice_for_character(dialogue["speaker"]),
        )
        
        return video
    
    def _generate_scene_clip(self, board: dict) -> str:
        """生成场景视频"""
        # 选择视频生成模型
        if "action" in board["prompt"].lower() or "movement" in board["prompt"].lower():
            # 动作场景用 Kling (动作更好)
            video = self.kling_client.generate(
                prompt=board["prompt"],
                duration=board["duration"],
                aspect_ratio="9:16"
            )
        else:
            # 静态场景用 Runway (质量更好)
            video = self.runway_client.generate(
                model="gen-3-alpha",
                prompt=board["prompt"],
                duration=board["duration"],
                aspect_ratio="9:16"
            )
        
        return video
    
    def _extract_dialogue(self, board: dict) -> dict:
        """从分镜中提取对话"""
        # 需要与剧本解析结果关联
        # 简化示例
        return {"speaker": "主角", "text": "对话内容"}
    
    def _select_avatar(self, character_name: str) -> str:
        """选择角色对应的数字人模型"""
        avatar_map = {
            "主角": "avatar_protagonist_001",
            "反派": "avatar_antagonist_001",
            "配角 A": "avatar_supporting_001",
        }
        return avatar_map.get(character_name, "avatar_default")
    
    def _get_voice_for_character(self, character_name: str) -> str:
        """获取角色对应的语音"""
        voice_map = {
            "主角": "elevenlabs_male_young",
            "反派": "elevenlabs_male_deep",
            "配角 A": "elevenlabs_female_warm",
        }
        return voice_map.get(character_name, "elevenlabs_default")
```

### 2.5 后期制作 Agent
```python
class PostProductionAgent:
    def __init__(self):
        self.video_clips = []
    
    def assemble_episode(self, video_clips: List[List[str]], music_style: str = "dramatic"):
        """组装完整剧集"""
        from moviepy.editor import *
        
        # 1. 加载所有视频片段
        clips = []
        for scene_clips in video_clips:
            for clip_path in scene_clips:
                video = VideoFileClip(clip_path)
                clips.append(video)
        
        # 2. 添加转场
        clips_with_transitions = []
        for i, clip in enumerate(clips):
            if i > 0:
                # 添加 0.3 秒交叉淡入淡出
                clip = clip.crossfadein(0.3)
            clips_with_transitions.append(clip)
        
        # 3. 拼接所有片段
        final_video = concatenate_videoclips(clips_with_transitions, method="compose")
        
        # 4. 生成背景音乐
        music = self._generate_background_music(
            duration=final_video.duration,
            style=music_style
        )
        music_audio = AudioFileClip(music)
        
        # 调整音乐音量 (低于人声)
        music_audio = music_audio.volumex(0.3)
        
        # 5. 混合音频
        if final_video.audio:
            final_audio = CompositeAudioClip([final_video.audio, music_audio])
        else:
            final_audio = music_audio
        
        final_video = final_video.set_audio(final_audio)
        
        # 6. 自动生成字幕
        subtitles = self._generate_subtitles(final_video)
        if subtitles:
            final_video = CompositeVideoClip([final_video] + subtitles)
        
        # 7. 调色统一
        final_video = self._apply_color_grading(final_video)
        
        # 8. 导出
        output_path = "final_episode.mp4"
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='h264',
            audio_codec='aac'
        )
        
        return output_path
    
    def _generate_background_music(self, duration: int, style: str) -> str:
        """使用 AI 生成背景音乐"""
        from suno_api import generate_music
        
        prompt = f"{style} background music for short drama, emotional, cinematic"
        
        music = generate_music(
            prompt=prompt,
            duration=min(duration, 120),  # Suno 最长 120 秒
            instrumental=True
        )
        
        return music
    
    def _generate_subtitles(self, video):
        """自动生成字幕"""
        import whisper
        
        # 提取音频
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path)
        
        # 语音识别
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="zh")
        
        # 生成字幕片段
        subtitle_clips = []
        for segment in result["segments"]:
            subtitle = TextClip(
                segment["text"],
                fontsize=24,
                color='white',
                stroke_color='black',
                stroke_width=1
            )
            subtitle = subtitle.set_position(('center', 'bottom'))
            subtitle = subtitle.set_start(segment["start"])
            subtitle = subtitle.set_duration(segment["end"] - segment["start"])
            subtitle_clips.append(subtitle)
        
        return subtitle_clips
    
    def _apply_color_grading(self, video):
        """应用色彩分级"""
        # 使用 colour-science 进行调色
        # 简化示例：调整对比度和饱和度
        pass
```

---

## 三、完整工作流程实战 (12min)

### 3.1 项目配置
```yaml
# project_config.yaml
project:
  name: "霸道总裁爱上我"
  genre: "romance_drama"
  total_episodes: 80
  episode_duration: 90  # seconds
  
visual_style:
  reference_images:
    - "references/mood_board_01.jpg"
    - "references/mood_board_02.jpg"
  color_palette:
    - "#FF6B6B"  # 浪漫红
    - "#4ECDC4"  # 清新蓝
    - "#FFE66D"  # 温暖黄
  lighting: "soft_romantic"

characters:
  - name: "林总"
    role: "protagonist"
    gender: "male"
    age: "28-32"
    avatar_id: "avatar_ceo_001"
    voice_id: "elevenlabs_male_deep"
  
  - name: "小雅"
    role: "protagonist"
    gender: "female"
    age: "22-26"
    avatar_id: "avatar_girl_001"
    voice_id: "elevenlabs_female_sweet"

video_generation:
  primary_model: "kling-1.5"  # 动作场景
  secondary_model: "runway-gen3"  # 静态场景
  digital_human: "heygen"
  
post_production:
  music_style: "emotional_piano"
  subtitle: true
  color_grading: "warm_romantic"
  
output:
  resolution: "1080x1920"  # 竖屏
  fps: 24
  format: "mp4"
```

### 3.2 一键生成脚本
```python
#!/usr/bin/env python3
"""
短剧自动化生成 - 从剧本到成片
Usage: python generate_drama.py script.md --config config.yaml
"""

import yaml
import argparse
from agents import (
    ScriptAnalyzer,
    StoryboardAgent,
    VideoGenerationAgent,
    PostProductionAgent
)

def main():
    parser = argparse.ArgumentParser(description='AI 短剧生成器')
    parser.add_argument('script', help='剧本文件路径')
    parser.add_argument('--config', default='config.yaml', help='配置文件')
    parser.add_argument('--output', default='output', help='输出目录')
    args = parser.parse_args()
    
    # 加载配置
    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print(f"🎬 开始生成短剧：{config['project']['name']}")
    
    # Step 1: 剧本分析
    print("\n📝 Step 1: 分析剧本...")
    analyzer = ScriptAnalyzer()
    with open(args.script, 'r', encoding='utf-8') as f:
        script_text = f.read()
    analysis = analyzer.analyze(script_text)
    print(f"  ✓ 识别 {analysis.total_scenes} 个场景")
    print(f"  ✓ 总时长约 {analysis.total_duration} 秒")
    print(f"  ✓ 主要角色：{', '.join([c.name for c in analysis.main_characters])}")
    
    # Step 2: 分镜生成
    print("\n🎨 Step 2: 生成分镜...")
    storyboard_agent = StoryboardAgent()
    style_refs = config['visual_style']['reference_images']
    storyboards = storyboard_agent.generate_storyboard(args.script, style_refs[0])
    print(f"  ✓ 生成 {sum(len(sb['storyboards']) for sb in storyboards)} 个分镜")
    
    # Step 3: 视频生成
    print("\n🎥 Step 3: 生成视频片段...")
    video_agent = VideoGenerationAgent()
    video_clips = video_agent.generate_scene_videos(storyboards)
    total_clips = sum(len(clips) for clips in video_clips)
    print(f"  ✓ 生成 {total_clips} 个视频片段")
    
    # Step 4: 后期合成
    print("\n✂️ Step 4: 后期合成...")
    post_agent = PostProductionAgent()
    music_style = config['post_production']['music_style']
    final_video = post_agent.assemble_episode(video_clips, music_style)
    print(f"  ✓ 成品输出：{final_video}")
    
    # Step 5: 质量检查
    print("\n🔍 Step 5: 质量检查...")
    quality_score = check_video_quality(final_video)
    print(f"  ✓ 质量评分：{quality_score}/1.0")
    
    if quality_score