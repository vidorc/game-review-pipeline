import os
import yaml
from pathlib import Path

def load_config(config_path=None):
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "default.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
    return path
