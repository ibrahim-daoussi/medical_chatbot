import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s') 


list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "experiment.py",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "templates/chat.html",
]


for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir, filename = os.path.split(file_path)

    if not file_dir == "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Created directory: {file_dir} for the file {filename}")
    if (not os.path.exists(file_path)) or os.path.getsize(file_path) == 0:
        with open(file_path, "w") as f:
            pass
        logging.info(f"Created file: {file_path}")
    else:  
        logging.info(f"File already exists: {file_path}, skipping creation.")
    