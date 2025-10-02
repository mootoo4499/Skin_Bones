# Setup Guide for New Screenplay Projects

*How to start a new screenplay project using this template*

---

## Quick Start (5 minutes)

### 1. Copy the Global Folder
```bash
# From your existing screenplay project
cp -r .global /path/to/new-screenplay-project/
```

### 2. Create Folder Structure
```bash
cd /path/to/new-screenplay-project
mkdir master staging versions research
```

### 3. Install Dependencies
```bash
# Install all tools from global package.json
cd .global/system_context
npm install

# This installs:
# - afterwriting-cli (Fountain → PDF)
# - markdown-pdf (Markdown → PDF)
# - fountain-js (screenplay analysis)
# - axios, cheerio (web research)
# - natural (NLP for dialogue analysis)
# - fs-extra, chalk (utilities)
```

### 4. Copy & Customize .cursorrules
```bash
# Copy template
cp .global/.cursorrules_template .cursorrules

# Edit to add your project-specific info:
# - Title
# - Characters
# - Logline
# - Genre
```

### 5. Start Writing
```bash
# Create your screenplay in staging
touch staging/Your_Title_Script_v0_[timestamp].fountain
touch staging/Your_Title_Treat_v0_[timestamp].md
```

---

## What Gets Reused vs What's Project-Specific

### Reused from .global/ (same for every project):
- ✅ Screenwriting craft knowledge (Expert_Advice_Hub.md)
- ✅ Fountain specification
- ✅ PDF generation tools
- ✅ Workflow automation rules
- ✅ package.json dependencies
- ✅ .cursorrules template

### Project-Specific (unique to each screenplay):
- Your screenplay content
- Your treatment
- Your research notes
- Character/location/historical context
- Customized .cursorrules (imports from .global but adds project details)

---

## Folder Structure Explanation

```
/YourNewProject/
├── /.global/          Copy this entire folder from previous project
├── /master/           Create empty, will populate automatically
├── /staging/          Create empty, start writing here
├── /versions/         Create empty, archives automatically
├── /research/         Create empty, add your notes
├── .cursorrules       Copy template, customize
└── README.md          Describe your project
```

---

## First-Time System Setup (One-Time Ever)

If this is your FIRST screenplay project with this system:

### Install Node.js
```bash
# Download from nodejs.org
# Verify installation:
node --version
npm --version
```

### Install Global Tools
```bash
npm install -g afterwriting-cli
npm install -g markdown-pdf
```

### Verify Installation
```bash
afterwriting --version
markdown-pdf --help
```

---

## Troubleshooting

### "afterwriting: command not found"
- Run: `npm install -g afterwriting-cli`
- Restart terminal

### "markdown-pdf: command not found"
- Run: `npm install -g markdown-pdf`
- Or install pandoc as alternative

### PDFs not generating
- Check that .fountain file has no syntax errors
- Try manual export first to isolate issue
- Check console for error messages

---

## That's It!

Once set up, the workflow "just works":
1. Edit in `/staging/`
2. Approve changes
3. AI syncs to `/master/` and generates PDFs automatically
4. Old versions archived
5. Treatment stays in sync

**Template this for every future screenplay. Five-minute setup, then focus on writing.**


