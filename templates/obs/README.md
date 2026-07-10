# OBS Dual Recording Setup

This setup records a **4K canvas** and outputs both a 16:9 video (for long‑form reviews) and a cropped 9:16 video (for shorts/reels) simultaneously. It requires a PC with a 4K-capable GPU and the **Source Record** OBS plugin.

## Installation

1. Install the [Source Record](https://obsproject.com/forum/resources/source-record.1285/) plugin.
2. In OBS, go to **Scene Collection → Import** and select the exported scene collection (coming soon: a pre‑exported `.zip` file). For now, manually recreate the scenes described below.
3. Set your base canvas to **3840×2160** (4K).
4. Add a **Game Capture** source and size it to fill the canvas.
5. Add a second scene, add a **Game Capture** source again, but crop it to **1080×1920** (vertical) using the transform tools.
6. In the Source Record filter, assign the main scene to record to a 16:9 file, and the vertical scene to a 9:16 file.
7. Start recording – you’ll get two videos.

See the full documentation in `docs/setup-guide.md` for detailed steps.
