# PurrfectKit

**PurrfectKit** is a whimsical Python library that blends feline charm with powerful NLP functionality. Inspired by Thai cat breeds, each module in the `purrfectmeow` package maps to a specific NLP technique—making text processing both fun and efficient.


## 🐾 Overview

PurrfectKit's core modules are each inspired by a Thai cat breed:

- **`purrfectmeow.Kornja`** – Breaks text into manageable segments *(Content Chunking)*.
- **`purrfectmeow.WichienMaat`** – Understands query intent for precise results *(Semantic Search)*.
- **`purrfectmeow.KhaoManee`** – Converts text to vectors and stores them *(Embedding & Storage)*.
- **`purrfectmeow.Malet`** – Extracts data from PDFs, images, spreadsheets, and Markdown *(Text Extraction)*.
- **`purrfectmeow.Suphalaks`** – Handles file operations and model/tokenizer loading to support other components *(Utility & Infrastructure)*

> **Note:** All modules are prefixed with `purrfectmeow` for namespace clarity and reflect Thai cat breed names.


## 🚀 Installation

Ensure you have **Python 3.10+** installed. Then, clone and install PurrfectKit locally:

```bash
git clone https://github.com/suwalutions/PurrfectKit.git
cd PurrfectKit
pip install -e .
```

## 🐱 Quick Start

Here's a simple example using the Malet class to extract text from a PDF:

```python
from purrfectmeow import Malet

try:
    docs = Malet.loader("example.pdf", "example.pdf", loader="PYMUPDF")
    print("Extracted text:", docs[:200])
except FileNotFoundError:
    print("Error: File 'example.pdf' not found.")
except ValueError as e:
    print(f"Error: {e}")
```

For more examples, see the [Usage Guide]().


## 📚 Documentation

* [Usage Guide](): Detailed examples for purrfectmeow.Malet.

* [API Reference](): Full API documentation for all modules.


## 📄 License

PurrfectKit is released under the terms of the [LICENSE](LICENSE) file.