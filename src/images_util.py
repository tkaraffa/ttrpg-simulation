import os
from pathlib import Path


def get_images_directory():
    images_directory = os.path.join(os.path.dirname(__file__), "images")
    Path(images_directory).mkdir(parents=True, exist_ok=True)
    return images_directory
