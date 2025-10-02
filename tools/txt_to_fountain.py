#!/usr/bin/env python3
"""
TXT to Fountain Screenplay Converter

Converts plain-text screenplay files to Fountain format for better machine readability.
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ConversionStats:
    """Statistics for a converted file."""
    file_path: str
    total_lines: int
    scene_headings: int = 0
    characters: int = 0
    dialogue_blocks: int = 0
    parentheticals: int = 0
    transitions: int = 0
    subheaders: int = 0
    shots: int = 0
    action_lines: int = 0
    ambiguous_lines: int = 0
    unparsed_lines: int = 0

class TextNormalizer:
    """Normalizes text for consistent parsing."""
    
    def __init__(self):
        self.page_number_pattern = re.compile(r'^\s*\d+\s*$')
        self.smart_quotes_pattern = re.compile(r'[\u201C\u201D\u2018\u2019\u0027]')
        self.em_dash_pattern = re.compile(r'\u2014')
        self.en_dash_pattern = re.compile(r'\u2013')
        
    def normalize(self, text: str) -> str:
        """Normalize text for consistent parsing."""
        # Remove page numbers
        if self.page_number_pattern.match(text.strip()):
            return ""
        
        # Normalize quotes
        text = self.smart_quotes_pattern.sub('"', text)
        
        # Normalize dashes
        text = self.em_dash_pattern.sub('--', text)
        text = self.en_dash_pattern.sub('-', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        return text

class LineClassifier:
    """Classifies lines into screenplay elements."""
    
    def __init__(self, patterns_file: Optional[str] = None):
        self.patterns = self._load_patterns(patterns_file)
        self.stats = defaultdict(int)
        
    def _load_patterns(self, patterns_file: Optional[str]) -> Dict[str, re.Pattern]:
        """Load regex patterns from file or use defaults."""
        default_patterns = {
            'scene_heading': re.compile(r'^(INT\.|EXT\.|INT\./EXT\.|I/E\.)[^\n]+( - (DAY|NIGHT|DAWN|DUSK|EVENING|MORNING|CONTINUOUS|MOMENTS LATER))?$', re.IGNORECASE),
            'character': re.compile(r'^[A-Z0-9 .()\'\-]{2,30}$'),
            'parenthetical': re.compile(r'^\([^\n]{1,80}\)$'),
            'transition': re.compile(r'^[A-Z ]+TO:$|^(FADE IN|FADE OUT|DISSOLVE TO|SMASH CUT TO):$', re.IGNORECASE),
            'subheader': re.compile(r'^[A-Z][A-Z ]{1,29}$'),
            'shot': re.compile(r'^(CLOSE ON|WIDE SHOT|POV|ANGLE ON|INSERT|ON):', re.IGNORECASE),
        }
        
        if patterns_file and os.path.exists(patterns_file):
            try:
                with open(patterns_file, 'r') as f:
                    custom_patterns = json.load(f)
                for key, pattern_str in custom_patterns.items():
                    if key in default_patterns:
                        default_patterns[key] = re.compile(pattern_str, re.IGNORECASE)
            except Exception as e:
                logging.warning(f"Could not load patterns file {patterns_file}: {e}")
                
        return default_patterns
    
    def classify_line(self, line: str, context: Dict = None) -> Tuple[str, str]:
        """Classify a line into screenplay element type."""
        if not line.strip():
            return "blank", ""
            
        line = line.strip()
        
        # Check patterns in order of specificity
        for element_type, pattern in self.patterns.items():
            if pattern.match(line):
                self.stats[element_type] += 1
                return element_type, line
                
        # Check for dialogue (follows character or parenthetical)
        if context and context.get('expecting_dialogue'):
            self.stats['dialogue'] += 1
            return "dialogue", line
            
        # Default to action
        self.stats['action'] += 1
        return "action", line

class BlockAssembler:
    """Assembles lines into screenplay blocks."""
    
    def __init__(self):
        self.current_block = []
        self.current_character = None
        self.current_parenthetical = None
        
    def add_line(self, line_type: str, line_content: str) -> List[Dict]:
        """Add a line and return completed blocks."""
        completed_blocks = []
        
        if line_type == "blank":
            if self.current_block:
                completed_blocks.append(self._finalize_block())
                self._reset_block()
            return completed_blocks
            
        if line_type == "character":
            if self.current_block:
                completed_blocks.append(self._finalize_block())
            self._reset_block()
            self.current_character = line_content
            self.current_block.append({"type": "character", "content": line_content})
            
        elif line_type == "parenthetical":
            if self.current_character:
                self.current_parenthetical = line_content
                self.current_block.append({"type": "parenthetical", "content": line_content})
            else:
                # Orphaned parenthetical, treat as action
                completed_blocks.append({"type": "action", "content": line_content})
                
        elif line_type == "dialogue":
            if self.current_character:
                self.current_block.append({"type": "dialogue", "content": line_content})
            else:
                # Orphaned dialogue, treat as action
                completed_blocks.append({"type": "action", "content": line_content})
                
        else:
            # Other element types (scene_heading, transition, etc.)
            if self.current_block:
                completed_blocks.append(self._finalize_block())
                self._reset_block()
            completed_blocks.append({"type": line_type, "content": line_content})
            
        return completed_blocks
    
    def _finalize_block(self) -> Dict:
        """Finalize the current block."""
        if not self.current_block:
            return {"type": "action", "content": ""}
            
        block = {
            "type": "character_block",
            "character": self.current_character,
            "parenthetical": self.current_parenthetical,
            "dialogue": []
        }
        
        for item in self.current_block:
            if item["type"] == "dialogue":
                block["dialogue"].append(item["content"])
                
        return block
    
    def _reset_block(self):
        """Reset the current block."""
        self.current_block = []
        self.current_character = None
        self.current_parenthetical = None

class FountainEmitter:
    """Emits Fountain format from parsed blocks."""
    
    def emit(self, blocks: List[Dict]) -> str:
        """Convert blocks to Fountain format."""
        fountain_lines = []
        
        for block in blocks:
            if block["type"] == "scene_heading":
                fountain_lines.append(block["content"])
                
            elif block["type"] == "character_block":
                fountain_lines.append(block["character"])
                if block["parenthetical"]:
                    fountain_lines.append(block["parenthetical"])
                for dialogue_line in block["dialogue"]:
                    fountain_lines.append(dialogue_line)
                fountain_lines.append("")  # Blank line after dialogue
                
            elif block["type"] == "transition":
                fountain_lines.append(block["content"])
                
            elif block["type"] == "subheader":
                fountain_lines.append(block["content"])
                
            elif block["type"] == "shot":
                fountain_lines.append(block["content"])
                
            else:  # action, dialogue, etc.
                fountain_lines.append(block["content"])
                
        return "\n".join(fountain_lines)

class TXTToFountainConverter:
    """Main converter class."""
    
    def __init__(self, patterns_file: Optional[str] = None):
        self.normalizer = TextNormalizer()
        self.classifier = LineClassifier(patterns_file)
        self.assembler = BlockAssembler()
        self.emitter = FountainEmitter()
        
    def convert_file(self, input_path: str, output_path: str) -> ConversionStats:
        """Convert a single file."""
        stats = ConversionStats(file_path=input_path, total_lines=0)
        
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            stats.total_lines = len(lines)
            
            # Process lines
            all_blocks = []
            context = {}
            
            for line in lines:
                normalized = self.normalizer.normalize(line)
                if not normalized:
                    continue
                    
                line_type, line_content = self.classifier.classify_line(normalized, context)
                
                if line_type == "character":
                    context['expecting_dialogue'] = True
                elif line_type in ["scene_heading", "transition", "subheader", "shot"]:
                    context['expecting_dialogue'] = False
                    
                blocks = self.assembler.add_line(line_type, line_content)
                all_blocks.extend(blocks)
                
            # Finalize any remaining block
            final_block = self.assembler._finalize_block()
            if final_block["type"] != "action" or final_block["content"]:
                all_blocks.append(final_block)
                
            # Emit Fountain
            fountain_content = self.emitter.emit(all_blocks)
            
            # Write output
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(fountain_content)
                
            # Update stats
            stats.scene_headings = self.classifier.stats['scene_heading']
            stats.characters = self.classifier.stats['character']
            stats.dialogue_blocks = self.classifier.stats['dialogue']
            stats.parentheticals = self.classifier.stats['parenthetical']
            stats.transitions = self.classifier.stats['transition']
            stats.subheaders = self.classifier.stats['subheader']
            stats.shots = self.classifier.stats['shot']
            stats.action_lines = self.classifier.stats['action']
            
        except Exception as e:
            logging.error(f"Error converting {input_path}: {e}")
            
        return stats

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Convert TXT screenplays to Fountain format")
    parser.add_argument("--input", "-i", required=True, help="Input file or directory")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Print summary only")
    parser.add_argument("--log", help="Log file for detailed output")
    parser.add_argument("--workers", type=int, default=1, help="Number of parallel workers")
    parser.add_argument("--patterns", help="JSON file with custom regex patterns")
    
    args = parser.parse_args()
    
    # Setup logging
    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
        
    converter = TXTToFountainConverter(args.patterns)
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    
    if input_path.is_file():
        # Single file
        output_path = output_dir / f"{input_path.stem}.fountain"
        stats = converter.convert_file(str(input_path), str(output_path))
        
        if args.dry_run:
            print(f"Would convert {input_path} -> {output_path}")
            print(f"Stats: {stats}")
        else:
            print(f"Converted {input_path} -> {output_path}")
            
    elif input_path.is_dir():
        # Directory
        txt_files = list(input_path.rglob("*.txt"))
        
        if args.dry_run:
            print(f"Would convert {len(txt_files)} files from {input_path}")
            for txt_file in txt_files:
                rel_path = txt_file.relative_to(input_path)
                output_path = output_dir / rel_path.with_suffix('.fountain')
                print(f"  {txt_file} -> {output_path}")
        else:
            print(f"Converting {len(txt_files)} files...")
            for txt_file in txt_files:
                rel_path = txt_file.relative_to(input_path)
                output_path = output_dir / rel_path.with_suffix('.fountain')
                stats = converter.convert_file(str(txt_file), str(output_path))
                print(f"Converted {txt_file} -> {output_path}")
    else:
        print(f"Error: {input_path} is not a file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main()
