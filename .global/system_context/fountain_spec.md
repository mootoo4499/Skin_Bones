# Fountain Specification for AI Systems

*Reference documentation for understanding Fountain screenplay format*

Source: [fountain.io](https://fountain.io) and [GitHub - nyousefi/Fountain](https://github.com/nyousefi/Fountain)

---

## What is Fountain?

Fountain is a simple markup syntax for writing screenplays in plain text. It's human-readable, future-proof, and converts to industry-standard screenplay PDFs.

**Key Principle**: "When viewed in plain text, your screenplay should feel like a screenplay."

---

## Core Syntax Rules

### Scene Headings
```
INT. LOCATION - TIME #1#
EXT. LOCATION - TIME #2#
INT./EXT. LOCATION - TIME #3#
```

Must start with INT, EXT, INT./EXT followed by period and space.

### Action/Description
Plain paragraphs of text. Keep to 2-4 lines maximum for readability.

```
Jamie walks across the dock. The sun is setting behind her.

She stops. Looks back at the water.
```

### Character Names
ALL CAPS on its own line, centered in PDF output.

```
JAMIE
```

### Dialogue
Text immediately following a character name, indented in PDF output.

```
JAMIE
I found it. The map is real.
```

### Parentheticals
Wrapped in parentheses under character name, before dialogue.

```
JAMIE
(whispering)
We need to go. Now.
```

### Transitions
RIGHT-ALIGNED in PDF. Must be all caps ending with "TO:".

```
CUT TO:

FADE OUT.
```

### Scene Numbers
Optional. Wrapped in #.

```
INT. KITCHEN - MORNING #4#
```

### Title Page
Key-value pairs at the start of the document.

```
Title: TIDE RUNNERS
Author: Kevin Samy
Draft date: October 1, 2025
```

---

## PDF Output Formatting

When Fountain converts to PDF, it applies industry-standard screenplay formatting:

- **Font**: Courier 12pt (or Courier Prime)
- **Page Margins**: 1" top/bottom/right, 1.5" left
- **Character Names**: Centered, 3.7" from left edge
- **Dialogue**: 2.5" from left edge, max 3.5" wide
- **Parentheticals**: 3.1" from left edge
- **Action**: Full width (1.5" to 7.5")
- **Scene Headings**: Full width, all caps
- **Page Numbers**: Top right
- **Approximate Timing**: 1 page = 1 minute of screen time

---

## Important for AI Understanding

1. **Fountain is the source format** - Your screenplay IS Fountain
2. **PDF is the output format** - Generated from Fountain for sharing/production
3. **Don't mix them** - Write in Fountain, export to PDF
4. **Parsers available**: afterwriting-cli, screenplain, Better Fountain extension
5. **It's NOT Markdown** - Similar simplicity, but different syntax for screenplay-specific elements

---

## Tools for Conversion

### afterwriting-cli (Node.js)
```bash
afterwriting --source script.fountain --pdf output.pdf
```

### screenplain (Python)
```bash
screenplain script.fountain --pdf output.pdf
```

### Better Fountain (VS Code Extension)
- Command Palette: "Fountain: Export to PDF"
- Generates industry-standard screenplay PDFs

---

## Regular Expressions (for parsing)

The [Fountain GitHub repo](https://github.com/nyousefi/Fountain) provides comprehensive regex patterns for parsing:
- Scene headings: `^(INT|EXT|EST|INT\.?\/EXT|I\/E)\.? `
- Character names: `^[A-Z][A-Z\s]*$`
- Dialogue detection
- Transition detection

These are available if you need to build custom parsers or analyzers.

---

**For AI systems: When working with Fountain files, preserve the plain text formatting. The PDF generation tools handle all the complex layout. Your job is to write compelling story content in clean Fountain syntax.**

