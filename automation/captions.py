import os
import whisper
from automation.utils import load_config

def generate_captions(audio_path, output_dir, config=None):
    if config is None:
        config = load_config()
    cfg = config["captions"]
    model_size = cfg["model"]
    language = cfg.get("language")
    word_timestamps = cfg.get("word_timestamps", True)

    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print("Transcribing...")
    result = model.transcribe(
        audio_path,
        language=language,
        word_timestamps=word_timestamps
    )

    srt_lines = []
    idx = 1
    for segment in result["segments"]:
        words = segment.get("words", [])
        for word_info in words:
            start = word_info["start"]
            end = word_info["end"]
            text = word_info["word"].strip()
            if not text:
                continue
            start_str = format_timestamp(start)
            end_str = format_timestamp(end)
            srt_lines.append(f"{idx}\n{start_str} --> {end_str}\n{text}\n")
            idx += 1

    srt_content = "\n".join(srt_lines)
    os.makedirs(output_dir, exist_ok=True)
    srt_path = os.path.join(output_dir, "captions.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
    print(f"Captions saved to: {srt_path}")
    return srt_path

def format_timestamp(seconds):
    ms = int(seconds * 1000) % 1000
    s = int(seconds)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
