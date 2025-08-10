import json

def load_mission(file_path):
    """Load a mission JSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
