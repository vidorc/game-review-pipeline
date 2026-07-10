#!/bin/bash
mkdir -p automation config docs templates obs audacity thumbnails assets/{music,sfx,fonts,overlays,transitions} examples

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "game-review-pipeline"
version = "0.1.0"
description = "Automated pre-editing pipeline for game review videos"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.10"
dependencies = [
    "typer>=0.12",
    "pyyaml>=6.0",
    "openai-whisper>=20231117",
    "ffmpeg-python>=0.2.0",
    "watchdog>=4.0",
]

[project.scripts]
pipeline = "automation.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["automation"]
EOF

# Write other files (README, LICENSE, config, all .py) using same heredoc pattern
# (I'll skip the full content here for brevity – you already have them)
