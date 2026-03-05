#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Director Storyboard Generator
Demo script for the director-storyboard skill
"""

import json
from typing import List, Dict, Any

# Shot type definitions
SHOT_TYPES = {
    "ECU": "Extreme Close-Up",
    "CU": "Close-Up",
    "MS": "Medium Shot",
    "MLS": "Medium Long Shot",
    "LS": "Long Shot",
    "ELS": "Extreme Long Shot"
}

# Camera movement definitions
CAMERA_MOVEMENTS = {
    "static": "Static",
    "push_in": "Push In",
    "pull_out": "Pull Out",
    "pan_left": "Pan Left",
    "pan_right": "Pan Right",
    "tilt_up": "Tilt Up",
    "tilt_down": "Tilt Down",
    "truck_left": "Truck Left",
    "truck_right": "Truck Right",
    "follow": "Follow",
    "arc": "Arc",
    "handheld": "Handheld"
}

# Transition definitions
TRANSITIONS = {
    "cut": "Cut",
    "fade_in": "Fade In",
    "fade_out": "Fade Out",
    "dissolve": "Dissolve",
    "wipe": "Wipe",
    "match_cut": "Match Cut"
}


class StoryboardGenerator:
    """Storyboard Generator Class"""
    
    def __init__(self):
        self.memory_bank: List[Dict[str, Any]] = []
        self.shots: List[Dict[str, Any]] = []
    
    def add_shot(self, shot_number: str, shot_type: str, description: str,
                 movement: str, duration: int, transition: str,
                 audio: str = "", m2v_memory: Dict = None) -> None:
        """Add a shot to the storyboard"""
        shot = {
            "shot_number": shot_number,
            "shot_type": shot_type,
            "shot_type_name": SHOT_TYPES.get(shot_type, shot_type),
            "description": description,
            "movement": movement,
            "movement_name": CAMERA_MOVEMENTS.get(movement, movement),
            "duration": duration,
            "transition": transition,
            "transition_name": TRANSITIONS.get(transition, transition),
            "audio": audio,
            "m2v_memory": m2v_memory or {}
        }
        self.shots.append(shot)
        
        # Update memory bank
        if m2v_memory:
            self.memory_bank.append({
                "after_shot": shot_number,
                "memory": m2v_memory
            })
    
    def generate_table(self) -> str:
        """Generate shot sequence table"""
        lines = []
        lines.append("| Shot Number | Shot Type | Description | Movement | Duration | Transition |")
        lines.append("|-------------|-----------|-------------|----------|----------|------------|")
        
        for shot in self.shots:
            # Truncate long descriptions
            desc = shot["description"][:40] + "..." if len(shot["description"]) > 40 else shot["description"]
            lines.append(
                f"| {shot['shot_number']} | {shot['shot_type']} | {desc} | "
                f"{shot['movement_name']} | {shot['duration']}s | {shot['transition_name']} |"
            )
        
        return "\n".join(lines)
    
    def generate_detailed_shots(self) -> str:
        """Generate detailed shot descriptions"""
        lines = []
        
        for shot in self.shots:
            lines.append(f"### {shot['shot_number']} - Shot Description")
            lines.append("")
            lines.append(f"**Description**:")
            lines.append(shot["description"])
            lines.append("")
            lines.append(f"**Movement**: {shot['movement_name']}")
            lines.append("")
            lines.append(f"**Duration**: {shot['duration']} seconds")
            lines.append("")
            lines.append(f"**Transition**: {shot['transition_name']}")
            lines.append("")
            
            if shot["audio"]:
                lines.append(f"**Audio**: {shot['audio']}")
                lines.append("")
            
            if shot["m2v_memory"]:
                lines.append("**M2V Memory Points**:")
                for key, value in shot["m2v_memory"].items():
                    lines.append(f"- {key}: {value}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_m2v_memory_table(self) -> str:
        """Generate M2V memory bank table"""
        if not self.memory_bank:
            return ""
        
        lines = []
        lines.append("## Memory-to-Video (M2V) Memory Bank")
        lines.append("")
        lines.append("| After Shot | Memory Content | Key Elements |")
        lines.append("|------------|----------------|--------------|")
        
        for mem in self.memory_bank:
            memory_text = "; ".join([f"{k}: {v}" for k, v in mem["memory"].items()])
            elements = ", ".join(mem["memory"].keys())
            lines.append(f"| {mem['after_shot']} | {memory_text[:50]}... | {elements} |")
        
        return "\n".join(lines)
    
    def generate_full_storyboard(self, title: str, total_duration: str,
                                  style: str, target_audience: str) -> str:
        """Generate complete storyboard"""
        lines = []
        
        # Title and metadata
        lines.append(f"# {title} Storyboard")
        lines.append("")
        lines.append(f"**Duration**: {total_duration}")
        lines.append(f"**Style**: {style}")
        lines.append(f"**Target Audience**: {target_audience}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Shot sequence table
        lines.append("## Shot Sequence")
        lines.append("")
        lines.append(self.generate_table())
        lines.append("")
        
        # Detailed shot descriptions
        lines.append("## Detailed Shot Descriptions")
        lines.append("")
        lines.append(self.generate_detailed_shots())
        
        # M2V memory bank
        if self.memory_bank:
            lines.append(self.generate_m2v_memory_table())
            lines.append("")
        
        return "\n".join(lines)


def create_smartwatch_ad() -> str:
    """Create smartwatch commercial storyboard example"""
    generator = StoryboardGenerator()
    
    # Shot 1: ECU - Product reveal
    generator.add_shot(
        shot_number="SC01",
        shot_type="ECU",
        description="Smartwatch dial close-up. Screen gradually lights up from black, displaying time 10:08. Metal case reflects cool-toned highlights. Digital numbers are crisp and sharp.",
        movement="push_in",
        duration=4,
        transition="fade_in",
        audio="Music: Soft electronic sound fades in. Tech sound effects.",
        m2v_memory={
            "Product Color": "Silver metal case, black dial",
            "Lighting": "Cool toned, high-light reflections",
            "Display Content": "Digital time 10:08, white numbers"
        }
    )
    
    # Shot 2: CU - Interaction demo
    generator.add_shot(
        shot_number="SC02",
        shot_type="CU",
        description="Finger touches screen. UI interface smoothly transitions showing heart rate data 72bpm. Blue themed interface with简洁 modern icons.",
        movement="static",
        duration=3,
        transition="cut",
        audio="SFX: Light touch feedback sound",
        m2v_memory={
            "UI Color": "Blue theme, white numbers",
            "Display Content": "Heart rate 72bpm, blue ring",
            "Interaction": "Touch swipe"
        }
    )
    
    # Shot 3: MS - Usage scenario
    generator.add_shot(
        shot_number="SC03",
        shot_type="MS",
        description="Business person raises wrist to check time. White shirt cuff visible. Background shows blurred city skyline with glass towers reflecting morning light.",
        movement="truck_right",
        duration=5,
        transition="cut",
        audio="Music: Upbeat electronic rhythm",
        m2v_memory={
            "Wearer": "Business person, white shirt cuff",
            "Scene": "City buildings, glass tower background",
            "Time": "Morning, soft natural light"
        }
    )
    
    # Shot 4: LS - Exercise scenario
    generator.add_shot(
        shot_number="SC04",
        shot_type="LS",
        description="Wearer jogging on park trail. Wearing gray quick-dry sportswear. Watch sways slightly with running motion. Sunlight filters through tree leaves onto screen.",
        movement="follow",
        duration=6,
        transition="cut",
        audio="SFX: Running footsteps, bird ambient sound",
        m2v_memory={
            "Clothing": "Gray quick-dry sportswear",
            "Scene": "Park trail, green tree background",
            "Action": "Running posture, natural arm swing"
        }
    )
    
    # Shot 5: CU - Data display
    generator.add_shot(
        shot_number="SC05",
        shot_type="CU",
        description="Watch screen close-up showing exercise data: pace 5'30\"/km, distance 5.2km, calories 320kcal. Data updates in real-time.",
        movement="push_in",
        duration=4,
        transition="cut",
        audio="SFX: Data change notification sound",
        m2v_memory={
            "UI Theme": "Blue sport interface",
            "Display Data": "Pace, distance, calories",
            "Data Update": "Real-time dynamic change"
        }
    )
    
    # Shot 6: MS - Emotional expression
    generator.add_shot(
        shot_number="SC06",
        shot_type="MS",
        description="Wearer stops running, looks at watch with satisfaction and smiles. Deep breath. Sunlight on face. Background blurred.",
        movement="static",
        duration=4,
        transition="cut",
        audio="Music: Reaches emotional climax, warm and uplifting",
        m2v_memory={
            "Expression": "Satisfied smile, sense of achievement",
            "Lighting": "Morning light, warm tone",
            "Emotion": "Positive and upward, post-exercise joy"
        }
    )
    
    # Shot 7: ECU - Brand reveal
    generator.add_shot(
        shot_number="SC07",
        shot_type="ECU",
        description="Watch side button and case close-up. Metal brushed texture. Brand logo subtly visible. Exquisite craftsmanship details.",
        movement="arc",
        duration=4,
        transition="fade_out",
        audio="Music: Fades out, brand sound effect",
        m2v_memory={
            "Material": "Metal brushed finish",
            "Logo Position": "Crown side, exquisite engraving",
            "Texture": "Premium, precision"
        }
    )
    
    # Generate complete storyboard
    return generator.generate_full_storyboard(
        title="SmartWatch Pro X1 Commercial",
        total_duration="30 seconds",
        style="Tech, Clean, Premium",
        target_audience="Urban professionals, fitness enthusiasts, tech product lovers"
    )


if __name__ == "__main__":
    # Generate example storyboard
    storyboard = create_smartwatch_ad()
    print(storyboard)
    
    # Save to file
    with open("smartwatch_storyboard.md", "w", encoding="utf-8") as f:
        f.write(storyboard)
    
    print("\n Storyboard generated and saved to smartwatch_storyboard.md")
