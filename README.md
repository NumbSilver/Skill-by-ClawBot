# Skill-by-ClawBot

AI Agent Skills created by ClawBot (OpenClaw)

## Skills

### remotion-video

Enhanced Remotion video template creation skill with intelligent component matching, layout automation, and best practices.

**Features:**
- 🎬 Create Remotion video templates
- 🤖 Intelligent animation component matching
- 📐 Automated layout generation
- ✅ Best practices built-in
- 📝 Complete code examples
- 🌳 Component selection decision tree

**Quick Start:**
```bash
# Generate a new template
python scripts/generate_template.py TemplateName
```

**Key Rules:**
1. 🔖 Logo injection (zIndex: 900) - Mandatory
2. 🎨 Color system (import from '@/Utils/Color') - No hardcoding
3. 📍 Script position rules (>5 scripts avoid center)
4. ⏱️ CTA timing (last 3 seconds)

**Contents:**
```
remotion-video/
├── SKILL.md                      # Complete skill documentation
├── references/
│   ├── animation_components.md   # Animation component catalog
│   ├── component_structure.md    # Component creation guide
│   ├── layout_guidelines.md      # Layout and style rules
│   └── template_patterns.md      # Best practices
├── scripts/
│   └── generate_template.py      # Template generator
└── assets/                       # Resource files
```

## License

MIT
