import subprocess
from automation.utils import load_config

def clean_audio(input_path, output_path, config=None):
    if config is None:
        config = load_config()
    filter_chain = config["audio"]["filter_chain"]
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-af", filter_chain,
        "-y",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Cleaned audio saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cleaning audio:\n{e.stderr}")
        return False
