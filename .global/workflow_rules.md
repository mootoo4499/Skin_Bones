# Screenplay Project Workflow Rules

*Master/Staging/Versions sync protocol for screenplay projects*

---

## Folder Purposes

### `/staging/` - WORKING DIRECTORY
- All edits happen here
- Files named with `_v0_` to indicate work-in-progress
- Format: `Tide_Runners_Script_v0_10.01.25_1853.fountain`

### `/master/` - READ-ONLY AUTHORITATIVE
- Latest approved versions only
- NO version numbers in filename (that's the indicator)
- Includes auto-generated PDFs
- Format: `Tide_Runners_Script_10.01.25_1853.fountain`

### `/versions/` - HISTORICAL ARCHIVE
- Previous approved versions
- Incremental version numbers: v1, v2, v3...
- Source files only (no PDFs to save space)
- Format: `Tide_Runners_Script_v3_10.01.25_1445.fountain`

---

## The Workflow

### When User Edits Screenplay in Staging:

1. **After user approves changes**, AI asks:
   ```
   "The screenplay has been updated. Should I:
   1) Update the treatment to reflect these changes?
   2) Sync to master and generate PDFs?"
   ```

2. **If user says yes to treatment update**:
   - AI analyzes screenplay changes
   - Updates treatment accordingly
   - Asks for confirmation

3. **If user says yes to sync**:
   - Current master → archive to `/versions/` with incremented version number
   - Staging → copy to `/master/` with new timestamp (no version number)
   - Generate PDFs for both screenplay and treatment
   - Update staging files with new v0 timestamp

### When User Edits Treatment in Staging:

1. **AI detects treatment change**, STOPS immediately

2. **AI analyzes dependencies**:
   - New characters → affects: character intros, all dialogue, arc tracking
   - Location changes → affects: scene headers, references, descriptions
   - Plot changes → affects: story structure, beats, sequences
   - Dialogue changes → affects: character voice, subtext

3. **AI presents detailed plan**:
   ```
   "Treatment change detected: [description]
   
   This affects:
   - [X] scenes with character references
   - [Y] locations mentioned
   - [Z] plot beats requiring adjustment
   
   Plan:
   1) Update character intro in scene #3
   2) Change location references in scenes #7, #12, #28
   3) Adjust plot beat at midpoint (scene #35)
   
   Estimated scope: [X] edits across [Y] scenes
   
   Should I proceed?"
   ```

4. **User confirms** → AI executes systematically

5. **After screenplay edits complete** → trigger master sync (same as above)

---

## Naming Conventions

### Timestamps
- Format: `MM.DD.YY_HHMM` (Pacific Time, military time, nearest minute)
- Example: `10.01.25_1853` = October 1, 2025, 6:53 PM Pacific

### File Names
- **Script**: `Tide_Runners_Script_[version?]_[timestamp].fountain`
- **Treatment**: `Tide_Runners_Treat_[version?]_[timestamp].md`

### Version Indicators
- **v0**: Work in progress (staging only)
- **No version**: Current authoritative (master only)
- **v1, v2, v3...**: Historical archive (versions only)

Examples:
- Staging: `Tide_Runners_Script_v0_10.01.25_1853.fountain`
- Master: `Tide_Runners_Script_10.01.25_1853.fountain`
- Versions: `Tide_Runners_Script_v3_10.01.25_1445.fountain`

---

## PDF Generation

Automatically triggered when syncing to master:

```bash
# Screenplay PDF
afterwriting --source master/Tide_Runners_Script_[timestamp].fountain --pdf master/Tide_Runners_Script_[timestamp].pdf

# Treatment PDF
markdown-pdf master/Tide_Runners_Treat_[timestamp].md -o master/Tide_Runners_Treat_[timestamp].pdf
```

---

## Version Increment Logic

1. **Find highest version number** in `/versions/` folder
2. **Increment by 1**
3. **Archive current master** with new version number
4. **Copy staging → master** with new timestamp (no version)
5. **Update staging** v0 with same new timestamp

---

## Safety Checks

Before syncing to master:
- ✅ Screenplay has no syntax errors
- ✅ Treatment matches screenplay structure
- ✅ All cross-references valid
- ✅ Character names consistent
- ✅ Scene numbers sequential
- ✅ No broken dependencies

---

*This workflow ensures you always have: current work (staging/v0), latest approved (master/no version), and historical archive (versions/v1-vN).*


