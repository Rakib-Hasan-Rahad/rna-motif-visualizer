# Documentation Images

This folder contains screenshots for the RNA Motif Visualizer documentation.

## Current Images
- `1.png`, `2.png`, `3.png` - Existing screenshots

## Required Images for README.md

Add the following screenshots to complete the documentation:

| Filename | Description | Used In |
|----------|-------------|---------|
| `banner.png` | Main plugin banner showing the plugin in action | README header |
| `installation_steps.png` | Plugin Manager settings tab screenshot | Installation section |
| `installation_success.png` | Welcome message in PyMOL console | Installation verification |
| `quickstart_demo.png` | Loaded structure with colored motifs | Quick Start section |
| `console_suggestions.png` | Console output showing "Next steps" suggestions | Quick Start section |
| `data_sources.png` | Diagram showing data flow from different sources | Data Sources section |
| `color_legend.png` | Visual color legend showing all motif colors | Display section |
| `object_panel.png` | PyMOL object panel with motif objects | Display section |
| `instance_table.png` | Console output of instance table | Instance Explorer section |
| `instance_view.png` | Zoomed view of a single motif instance | Instance Explorer section |

## Required Images for TUTORIAL.md

| Filename | Description | Used In |
|----------|-------------|---------|
| `tutorial_welcome.png` | Welcome message after plugin loads | Getting Started |
| `tutorial_loaded.png` | Structure after `rna_load` command | Loading section |
| `tutorial_gnra.png` | GNRA motifs highlighted | Exploring Motifs |
| `tutorial_instance.png` | Single instance zoomed view | Instance Details |

## How to Create Screenshots

1. **In PyMOL**, run the commands shown in the tutorial
2. **Position the view** as desired
3. **Take screenshot** using:
   - macOS: `Cmd + Shift + 4` (select area)
   - Or in PyMOL: `png filename.png, dpi=150`
4. **Save to this folder** with the correct filename

## Recommended Settings for Screenshots

```python
# White background for clarity
bg_color white

# High quality rendering
set ray_shadows, 0
set antialias, 2

# Save high-res image
ray 1200, 900
png my_screenshot.png
```

## Tips

- Use **white background** for better visibility in documentation
- Crop images to focus on relevant areas
- Keep file sizes reasonable (< 500KB each)
- Use PNG format for screenshots
