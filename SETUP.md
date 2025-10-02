# Setup Guide

## For New Developers

### 1. Clone Repository
```bash
git clone https://github.com/mootoo4499/Skin_Bones.git
cd Skin_Bones
```

### 2. Install Dependencies
```bash
# Install Node.js tools
cd .global/system_context
npm install

# Install Python tools
pip install screenplain
```

### 3. Configure Neo4j (Optional)
- Set up Neo4j database
- Update credentials in `Neo4J/neo4j_config.py`

### 4. Start Working
- Edit files in `staging/` folder
- Follow workflow rules in `.global/workflow_rules.md`

## File Naming Convention

**Staging Files (Work-in-Progress):**
- `Skin_Bones_Script_v0_MM.DD.YY_HHMM.fountain`
- `Skin_Bones_Treat_v0_MM.DD.YY_HHMM.md`

**Master Files (Approved):**
- `Skin_Bones_Script_MM.DD.YY_HHMM.fountain`
- `Skin_Bones_Treat_MM.DD.YY_HHMM.md`

**Version Archive:**
- `Skin_Bones_Script_v1_MM.DD.YY_HHMM.fountain`
- `Skin_Bones_Script_v2_MM.DD.YY_HHMM.fountain`

## Workflow Commands

```bash
# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

## Global Guidance System

The `.global/` folder contains reusable frameworks:
- **Expert screenwriting advice** (comprehensive methodology)
- **Workflow automation** (Master/Staging sync)
- **Technical tools** (Fountain, PDF generation)
- **Templates** (treatment, cursor rules)

## Troubleshooting

**"afterwriting: command not found"**
```bash
npm install -g afterwriting-cli
```

**"markdown-pdf: command not found"**
```bash
npm install -g markdown-pdf
```

**Long filename errors on Windows**
- Git on Windows has filename length limits
- Some files in `Scripts_Corpus/` may not sync
- This doesn't affect core project functionality
