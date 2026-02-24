# config.py
import json
from dataclasses import dataclass

@dataclass
class AppConfig:
    window_width: int
    window_height: int
    initial_zoom: float
    initial_rotation_x: float
    initial_rotation_y: float

def load_config(path='config.json') -> AppConfig:
    with open(path, 'r') as f:
        data = json.load(f)
    return AppConfig(**data)

# --- Color Constants ---
BG =    (200, 200, 225)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE =  (0, 0, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)
GRAY =  (150, 150, 150)
