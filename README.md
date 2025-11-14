![PurrfectMeow Logo](https://github.com/suwalutions/PurrfectKit/blob/meow/docs/_static/repo-logo.png)

# PurrfectKit

[![Python 3.10–3.13](https://img.shields.io/badge/python-3.10–3.13-blue)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/purrfectkit?color=gold&label=PyPI)](https://pypi.org/project/purrfectkit/)
[![Downloads](https://img.shields.io/pypi/dm/purrfectkit?color=purple)](https://pypistats.org/packages/purrfectkit)
[![codecov](https://codecov.io/github/suwalutions/PurrfectKit/branch/meow/graph/badge.svg?token=Z6YETHJXCL)](https://codecov.io/github/suwalutions/PurrfectKit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Docker](https://img.shields.io/docker/v/suwalutions/purrfectkit?label=docker)](https://ghcr.io/suwalutions/purrfectkit)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)


**PurrfectKit** is your all-in-one, dependency-smart, configuration-friendly toolkit that turns even the most advanced Retrieval-Augmented Generation (RAG) workflows into a smooth, beginner-friendly experience.


🧩 5 Cats Will Lead You To The Purrfect Way.    

🐱 **Suphalak** – Seamlessly reads and loads content from files.

🐱 **Malet** – Splits content into high-quality, model-friendly chunks.

🐱 **WichienMaat** – Embeds chunks into powerful vector representations.

🐱 **KhaoManee** – Searches and retrieves the most relevant vectors.

🐱 **Kornja** – Generates final responses enriched by retrieved knowledge (Under Development).


> **_NOTE:_** The Thai cat-themed naming isn’t just cute—it makes learning and remembering the RAG process surprisingly fun and intuitive.


Whether you're a sturdent, researcher, hobbyist, or production-level engineer, this toolkit gives you a clean, guided workflow that “**just works**”

## Quickstart

PurrfectKit aims to be plug-and-play, but a few lightweight system tools are required.

### Prerequisites

#### Linux (Ubuntu / Debian)

    # Install Python (if not already)
    sudo apt update
    sudo apt install -y python3 python3-pip
    
    # Install Tesseract OCR
    sudo apt install -y tesseract-ocr tesseract-ocr-tha
    
    # Install FFmpeg
    sudo apt install -y ffmpeg
    
    # Install libmagic
    sudo apt install -y libmagic1

#### macOS

    # Install Homebrew if missing
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Install Python
    brew install python
    
    # Install Tesseract OCR
    brew install tesseract
    
    # Install FFmpeg
    brew install ffmpeg
    
    # Install libmagic
    brew install libmagic

#### Windows

    # Install Python
    Download from the official website:
   
    [https://www.python.org/downloads/](https://www.python.org/downloads/)

    ✔ Make sure to check “Add Python to **PATH**” during installation.

    # Install Tesseract OCR
    Download the Windows installer:

    [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

    ✔ Make sure to add the installation path to your **System PATH**



### Installation
```bash
pip install purrfectkit

```

### Usage
```python
from purrfectmeow.meow.felis import DocTemplate, MetaFile
from purrfectmeow import Suphalak, Malet, WichienMaat, KhaoManee

file_path = 'test/test.pdf'
metadata = MetaFile.get_metadata(file_path)
with open(file_path, 'rb') as f:
    content = Suphalak.reading(f, 'test.pdf')
chunks = Malet.chunking(content, chunk_method='token', chunk_size='500', chunk_overlap='25')
docs = DocTemplate.create_template(chunks, metadata)
embedding = WichienMaat.embedding(chunks)
query = WichienMaat.embedding("ทดสอบ")
KhaoManee.searching(query, embedding, docs, 2)

```

## License

PurrfectKit is released under the [MIT License](LICENSE).
