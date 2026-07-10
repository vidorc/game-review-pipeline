import os
from automation.utils import load_config, ensure_dir

def create_project_structure(base_dir: str, config=None):
    if config is None:
        config = load_config()
    folders = config["folders"]
    created = []
    for name in folders.values():
        path = os.path.join(base_dir, name)
        ensure_dir(path)
        created.append(path)
    return created
