#!/usr/bin/env python3
"""
生成 Remotion 视频模板的基础结构

Usage:
    generate_template.py <template-name> [--path <path>]

Examples:
    generate_template.py MyNewVideo
    generate_template.py MyNewVideo --path modules/motion-editor/src/remotion/VideoTemplate
"""

import sys
from pathlib import Path

TEMPLATE_TSX = """import {{
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
}} from 'remotion';
import {{ z }} from 'zod';
import {{ getVideoMetadata }} from '@remotion/media-utils';
import AnimationText from '@/remotion/AnimateComponent/Text';
import {{
  TextAnimationType,
  TextEffectType,
}} from '@/remotion/AnimateComponent/Text/constants';
import Container from '@/remotion/AnimateComponent/Container';
import {{
  ContainerAnimationType,
}} from '@/remotion/AnimateComponent/Container/constants';
import React from 'react';
import {{ primaryColors, neutralColors, rgbaColor }} from '@/Utils/Color';
import {{ TikTokSansText }} from '@/Utils/load-font';
import {{ staticPlatformCdn }} from '@/Utils/cdn';

export const {TemplateName}Schema = z.object({{
  src: z.string(),
  composition: z.string().optional(),
  endSrc: z.string(),
  segmentationArray: z.array(z.number()),
  segmentationArrayKeyWords: z.array(z.array(z.string())),
  _seed: z.number().optional(),
}});

// Template Meta Information
export const {TemplateName}TemplateMeta = {{
  zh: {{
    overview: '{TemplateName} 是一个专为特定场景设计的视频模板。',
    useCases: [
      '用例1',
      '用例2',
    ],
    keywords: [],
  }},
  en: {{
    overview: '{TemplateName} is a video template designed for specific scenarios.',
    useCases: [
      'Use case 1',
      'Use case 2',
    ],
    keywords: [],
  }},
}};

const globalMeta = {{
  mainDuration: 0,
  endDuration: 0,
}};

// 每句话的开始时间[第2句话开始时间，第3句话开始时间...音频结束时间]
const _segmentationArray = [
  50, 100, 150, 200, 250, 300, 350, 400, 450, 500,
];

// 每句话的KEYWords[第1句话keyWords[]，第2句话keyWords[]...]
const _segmentationArrayKeyWords = [
  ['keyWords1'],
  ['keyWords2'],
  ['keyWords3'],
  ['keyWords4'],
  ['keyWords5'],
];

export const calculate{TemplateName}Metadata: CalculateMetadataFunction<
  z.infer<typeof {TemplateName}Schema>
> = async ({{ props }}) => {{
  const fps = 30;
  try {{
    const metadata = await getVideoMetadata(props.src);
    globalMeta.mainDuration = Math.floor(metadata.durationInSeconds * fps);
    return {{
      fps,
      durationInFrames: globalMeta.mainDuration + 50,
    }};
  }} catch (error) {{
    console.error('获取视频元数据失败:', error);
    return {{
      fps,
      durationInFrames: 1630, // 默认值
    }};
  }}
}};

export const {TemplateName}: React.FC<
  z.infer<typeof {TemplateName}Schema>
> = ({{
  src,
  endSrc,
  composition,
  segmentationArray = _segmentationArray,
  segmentationArrayKeyWords = _segmentationArrayKeyWords,
}}) => {{
  const {{ width, durationInFrames }} = useVideoConfig();
  const frame = useCurrentFrame();

  const scriptCount = segmentationArrayKeyWords.length;
  
  return (
    <AbsoluteFill style={{{{ backgroundColor: neutralColors[0] }}}}>
      {/* Logo - 必须包含在每个模板中 */}
      <img
        src={{staticPlatformCdn('images/bailogo.png')}}
        style={{
          position: 'absolute',
          zIndex: '900',
          width: '70%',
          top: '2%',
          left: '15%',
        }}
      />
      <Series>
        <Series.Sequence durationInFrames={{durationInFrames}}>
          <Container
            animations={{[
              {{
                type: ContainerAnimationType.ZOOM_IN_BLUR,
                config: {{
                  animationDelay: durationInFrames,
                  animationDuration: 45,
                }},
              }},
            ]}}
          >
            <AbsoluteFill>
              {/* 主视频 */}
              <OffthreadVideo
                style={{
                  height: '100%',
                  width: '100%',
                  objectFit: 'cover',
                }}
                src={{src}}
                startFrom={{0}}
                endAt={{durationInFrames}}
                volume={{1}}
              />
            </AbsoluteFill>
            <AbsoluteFill>
              {/* 示例：第一个断句的文本 */}
              {{segmentationArray.length > 0 && (
                <Sequence
                  from={{segmentationArray[0]}}
                  durationInFrames={{segmentationArray[1] - segmentationArray[0] || 60}}
                >
                  <AnimationText
                    style={{
                      transform: 'skew(50deg)',
                      display: 'inline-block',
                      color: 'white',
                      fontSize: 80,
                      fontWeight: 1000,
                      zIndex: 100,
                      width: '100%',
                    }}
                    baseProps={{
                      content: segmentationArrayKeyWords[0]?.[0] || 'Default Text',
                      // 如果脚本数量超过5个，使用顶部位置；否则使用中部
                      position: segmentationArrayKeyWords.length > 5 ? [50, 25] : [50, 50],
                    }}
                    effects={{[
                      {{
                        type: TextEffectType.OUTLINE,
                        config: {{
                          outlineColor: neutralColors[5],  // 使用导入的白色，不要硬编码
                          thickness: 5,
                        }},
                      }},
                    ]}}
                    animations={{[
                      {{
                        type: TextAnimationType.POP,
                        config: {{
                          durationInFrames: 30,
                          trigger: 'onEnter',
                        }},
                      }},
                    ]}}
                  />
                </Sequence>
              )}}
              
              {/* 结束CTA */}
              <Sequence
                from={{segmentationArray[segmentationArray.length - 1] || durationInFrames - 120}}
                durationInFrames={{120}}
              >
                {/* 在这里添加结束CTA组件 */}
              </Sequence>
            </AbsoluteFill>
          </Container>
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
}};
"""


def generate_template(template_name, base_path=None):
    """
    生成模板文件
    
    Args:
        template_name: 模板名称（PascalCase）
        base_path: 基础路径，默认为当前目录
    """
    if base_path is None:
        base_path = Path.cwd()
    else:
        base_path = Path(base_path)
    
    template_dir = base_path / template_name
    template_file = template_dir / 'index.tsx'
    
    # 检查目录是否已存在
    if template_dir.exists():
        print(f"❌ 错误: 模板目录已存在: {template_dir}")
        return False
    
    try:
        # 创建目录
        template_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建模板目录: {template_dir}")
        
        # 生成模板文件
        template_content = TEMPLATE_TSX.replace('{TemplateName}', template_name)
        template_file.write_text(template_content, encoding='utf-8')
        print(f"✅ 创建模板文件: {template_file}")
        
        print(f"\n✅ 模板 '{template_name}' 生成成功！")
        print("\n下一步:")
        print(f"1. 编辑 {template_file} 实现具体的模板逻辑")
        print("2. 根据需要添加 composition.json（可选）")
        print("3. 在模板中使用合适的 AnimationComponent")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_template.py <template-name> [--path <path>]")
        print("\nExamples:")
        print("  generate_template.py MyNewVideo")
        print("  generate_template.py MyNewVideo --path modules/motion-editor/src/remotion/VideoTemplate")
        sys.exit(1)
    
    template_name = sys.argv[1]
    base_path = None
    
    # 解析 --path 参数
    if '--path' in sys.argv:
        path_index = sys.argv.index('--path')
        if path_index + 1 < len(sys.argv):
            base_path = sys.argv[path_index + 1]
    
    # 验证模板名称（应该是 PascalCase）
    if not template_name[0].isupper():
        print(f"⚠️  警告: 模板名称建议使用 PascalCase (例如: {template_name.capitalize()})")
    
    print(f"🚀 生成模板: {template_name}")
    if base_path:
        print(f"   位置: {base_path}")
    print()
    
    result = generate_template(template_name, base_path)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()


