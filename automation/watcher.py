import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from automation.utils import load_config

class GameCaptureHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        self.watch_settings = config.get("watcher", {})
        self.allowed_extensions = self.watch_settings.get("allowed_extensions", [".mp4", ".mkv"])
        self.auto_run = self.watch_settings.get("auto_run", False)
        self.voice_ext = self.watch_settings.get("voice_extension", ".wav")
        self.output_base = self.watch_settings.get("output_base_dir", "./output")
    
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = Path(event.src_path)
        if filepath.suffix.lower() not in self.allowed_extensions:
            return
        time.sleep(2)
        voice_file = filepath.with_suffix(self.voice_ext)
        if not voice_file.exists():
            print(f"No voiceover found for {filepath.name}. Skipping pipeline.")
            return
        print(f"Detected new recording: {filepath.name}")
        if self.auto_run:
            cmd = [
                "pipeline", "run",
                "--voice", str(voice_file),
                "--output-dir", str(Path(self.output_base) / filepath.stem)
            ]
            subprocess.run(cmd, check=True)
        else:
            print(f"Run manually: pipeline run --voice {voice_file} --output-dir {Path(self.output_base) / filepath.stem}")

def start_watcher(config_path=None):
    config = load_config(config_path)
    watch_dir = config["watcher"]["watch_folder"]
    if not watch_dir:
        print("❌ No watch_folder set in config. Please edit config/default.yaml and set watcher.watch_folder to the directory where OBS saves recordings.")
        return
    print(f"Watching folder: {watch_dir}")
    handler = GameCaptureHandler(config)
    observer = Observer()
    observer.schedule(handler, watch_dir, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
