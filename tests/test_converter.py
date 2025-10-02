#!/usr/bin/env python3
"""
Test cases for TXT to Fountain converter.
"""

import os
import tempfile
import unittest
from pathlib import Path
import sys

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from txt_to_fountain import TXTToFountainConverter

class TestTXTToFountainConverter(unittest.TestCase):
    
    def setUp(self):
        self.converter = TXTToFountainConverter()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_basic_scene_conversion(self):
        """Test basic scene heading and dialogue conversion."""
        input_content = """INT. LIVING ROOM - DAY

JOHN
Hello there.

MARY
Hi John, how are you?

JOHN
I'm doing well, thanks.
"""
        
        input_file = os.path.join(self.temp_dir, "test.txt")
        output_file = os.path.join(self.temp_dir, "test.fountain")
        
        with open(input_file, 'w') as f:
            f.write(input_content)
            
        stats = self.converter.convert_file(input_file, output_file)
        
        self.assertTrue(os.path.exists(output_file))
        self.assertEqual(stats.scene_headings, 1)
        self.assertEqual(stats.characters, 2)
        self.assertGreater(stats.dialogue_blocks, 0)
        
        with open(output_file, 'r') as f:
            output_content = f.read()
            
        self.assertIn("INT. LIVING ROOM - DAY", output_content)
        self.assertIn("JOHN", output_content)
        self.assertIn("MARY", output_content)
        
    def test_parenthetical_conversion(self):
        """Test parenthetical conversion."""
        input_content = """JOHN
(smiling)
Hello there.

MARY
(concerned)
Are you okay?
"""
        
        input_file = os.path.join(self.temp_dir, "test_parenthetical.txt")
        output_file = os.path.join(self.temp_dir, "test_parenthetical.fountain")
        
        with open(input_file, 'w') as f:
            f.write(input_content)
            
        stats = self.converter.convert_file(input_file, output_file)
        
        self.assertEqual(stats.parentheticals, 2)
        
        with open(output_file, 'r') as f:
            output_content = f.read()
            
        self.assertIn("(smiling)", output_content)
        self.assertIn("(concerned)", output_content)
        
    def test_transition_conversion(self):
        """Test transition conversion."""
        input_content = """INT. ROOM - DAY

Some action here.

CUT TO:

EXT. STREET - NIGHT

More action.
"""
        
        input_file = os.path.join(self.temp_dir, "test_transition.txt")
        output_file = os.path.join(self.temp_dir, "test_transition.fountain")
        
        with open(input_file, 'w') as f:
            f.write(input_content)
            
        stats = self.converter.convert_file(input_file, output_file)
        
        self.assertEqual(stats.transitions, 1)
        
        with open(output_file, 'r') as f:
            output_content = f.read()
            
        self.assertIn("CUT TO:", output_content)
        
    def test_subheader_conversion(self):
        """Test subheader conversion."""
        input_content = """INT. HOUSE - DAY

KITCHEN
John makes coffee.

LIVING ROOM
Mary reads a book.
"""
        
        input_file = os.path.join(self.temp_dir, "test_subheader.txt")
        output_file = os.path.join(self.temp_dir, "test_subheader.fountain")
        
        with open(input_file, 'w') as f:
            f.write(input_content)
            
        stats = self.converter.convert_file(input_file, output_file)
        
        self.assertEqual(stats.subheaders, 2)
        
        with open(output_file, 'r') as f:
            output_content = f.read()
            
        self.assertIn("KITCHEN", output_content)
        self.assertIn("LIVING ROOM", output_content)

if __name__ == "__main__":
    unittest.main()
