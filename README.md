# Manim Frame Review Skill

An Agent Skill for rendering Manim scenes to PNG frames and reviewing them quickly to diagnose animation and layout issues, based on the open format from https://agentskills.io/.

📦 **Download latest release:**
- [manim-skill.zip](https://github.com/DominikPeters/manim-skill/releases/latest/download/manim-skill.zip)
- [manim-skill.skill](https://github.com/DominikPeters/manim-skill/releases/latest/download/manim-skill.skill)

## Overview

This skill streamlines the Manim development workflow by providing scripts to:
- Render scenes to low-quality PNG frames for fast iteration
- Generate contact sheets (grid previews) of frames for quick visual inspection
- Customize rendering parameters (FPS, quality, format)

Use this skill when working on Manim scene debugging, verifying visual correctness, checking for overlaps/cropping, or inspecting frame-by-frame output.

Contributions are welcome!

## Contents

## Documentation

`SKILL.md` explains how to render manim scenes to PNG frames and review them.

## Scripts

- **`scripts/refresh_frames.py`**: Delete old frames, re-render a Manim scene, optionally generate contact sheet
  - Run with `--help` for full options

- **`scripts/make_contact_sheet.py`**: Build a contact sheet PNG from existing frames without re-rendering
  - Run with `--help` for full options
  - Requires Pillow for full features (gridlines, labels)
  - Falls back to ImageMagick if Pillow unavailable

## Resources

- **`references/manim-docs/`**: Local copy of Manim documentation (tutorials, guides, reference, FAQ) in markdown format for quick searching

## Example Animation

A simple Hello World test animation is included in `tools/test/hello_world.py` for testing the scripts.

```bash
python3 scripts/refresh_frames.py --contact-sheet tools/test/hello_world.py HelloWorld
```

## Dependencies

- Python 3.7+
- Manim Community
- Pillow (for high-quality contact sheets with labels and gridlines)
- ImageMagick (optional fallback for contact sheets)

## Releases

Releases are created automatically via GitHub Actions when Manim documentation is updated. Each release includes:
- `manim-skill.zip`: Complete skill package
- `manim-skill.skill`: Identical copy with `.skill` extension for easy import

Version bumping is automatic (semantic versioning: major.minor.patch).

## Automated Updates

- GitHub Actions runs `tools/update_manim_docs.py` on:
  - Every push to master
  - Weekly (Sundays at midnight UTC)
  - Manual dispatch via workflow_dispatch

If documentation changes are detected, they are committed and a release is created.

## License

MIT
