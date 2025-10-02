# PDF Generation Tools & Commands

*How to convert Fountain screenplays and Markdown treatments to professional PDFs*

---

## Screenplay: Fountain → PDF

### Primary Tool: Better Fountain Extension (Already Installed)

**You already have this!** Just use Command Palette.

**Usage**:
1. Open `.fountain` file in Cursor
2. Press `Ctrl+Shift+P` (Command Palette)
3. Type "Fountain: Export to PDF"
4. PDF generates automatically with proper screenplay formatting

**For Automation**: We'll use screenplain (Python) for command-line generation.

---

### Alternative Tool 1: screenplain (Python)

**Install**:
```bash
pip install screenplain
```

**Usage**:
```bash
# Generate PDF
screenplain script.fountain --pdf output.pdf

# Generate HTML (for preview)
screenplain script.fountain --format html > output.html
```

**In Our Workflow**:
```bash
# From project root
screenplain staging/Tide_Runners_Script_v0_10.01.25_1905.fountain --pdf master/Tide_Runners_Script_10.01.25_1905.pdf
```

**Features**:
- Industry-standard screenplay formatting
- Courier font, correct margins
- Fast and reliable
- Cross-platform (Windows/Mac/Linux)

---

### Alternative Tool 2: wrap (Cross-Platform CLI)

From [GitHub - Wraparound/wrap](https://github.com/Wraparound/wrap)

**Install**:
```bash
# Download binary for your OS from GitHub releases
# Or build from source
```

**Usage**:
```bash
wrap input.fountain output.pdf
```

---

## Treatment: Markdown → PDF

### Tool: markdown-pdf (Node.js)

**Install**:
```bash
npm install -g markdown-pdf
```

**Usage**:
```bash
# Basic conversion
markdown-pdf input.md -o output.pdf

# With custom styling
markdown-pdf input.md -o output.pdf -s styles.css
```

**In Our Workflow**:
```bash
markdown-pdf staging/Tide_Runners_Treat_v0_10.01.25_1905.md -o master/Tide_Runners_Treat_10.01.25_1905.pdf
```

---

### Alternative: Pandoc (Universal Converter)

**Install**:
```bash
# Windows (via Chocolatey)
choco install pandoc

# Or download from pandoc.org
```

**Usage**:
```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

**Features**:
- Highly customizable templates
- Professional output
- Supports complex formatting

---

## Recommended Setup

**For Full Automation**:
```bash
# Install Python tool for Fountain
pip install screenplain

# Install Node tool for Markdown
npm install -g markdown-pdf
```

**Then create automation script** (see below).

---

## Automation Script

Create `.global/system_context/scripts/generate-pdfs.js`:

```javascript
const { exec } = require('child_process');
const fs = require('fs-extra');
const path = require('path');

function generatePDFs(scriptPath, treatPath, outputDir) {
  const timestamp = new Date().toLocaleString('en-US', {
    timeZone: 'America/Los_Angeles',
    year: '2-digit',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).replace(/(\d+)\/(\d+)\/(\d+),?\s*(\d+):(\d+)/, '$1.$2.$3_$4$5');
  
  // Generate screenplay PDF
  exec(`screenplain "${scriptPath}" --pdf "${outputDir}/Tide_Runners_Script_${timestamp}.pdf"`,
    (error, stdout, stderr) => {
      if (error) {
        console.error('❌ Screenplay PDF error:', error.message);
      } else {
        console.log(`✅ Screenplay PDF generated: Tide_Runners_Script_${timestamp}.pdf`);
      }
  });
  
  // Generate treatment PDF
  exec(`markdown-pdf "${treatPath}" -o "${outputDir}/Tide_Runners_Treat_${timestamp}.pdf"`,
    (error, stdout, stderr) => {
      if (error) {
        console.error('❌ Treatment PDF error:', error.message);
      } else {
        console.log(`✅ Treatment PDF generated: Tide_Runners_Treat_${timestamp}.pdf`);
      }
  });
}

module.exports = { generatePDFs };
```

---

## Quality Verification

When PDFs are generated, verify:
- ✅ **Screenplay**: Courier 12pt, 1.5" left margin, 1" others
- ✅ **Scene headers**: All caps, full width
- ✅ **Character names**: Centered
- ✅ **Dialogue**: Properly indented
- ✅ **Page breaks**: At logical points
- ✅ **Title page**: Formatted correctly
- ✅ **~1 page = ~1 minute** runtime

---

## Manual Fallback

If automation fails, you can always:
1. Open `.fountain` file in Cursor
2. Command Palette → "Fountain: Export to PDF"
3. Save PDF to appropriate folder manually

**But the goal is full automation via screenplain + markdown-pdf.**
