# PurrfectKit

**PurrfectKit** is a whimsical Python library that blends feline charm with powerful natural language processing (NLP), optical character recognition (OCR), and document processing capabilities. Inspired by Thai cat breeds, each module in the `purrfectmeow` package maps to a specific technique, making text processing, semantic search, and data extraction both fun and efficient.

## 🐾 Overview

PurrfectKit combines NLP, OCR, and document processing with a playful nod to Thai cat breeds. Its core modules are:

- `purrfectmeow.Kornja` – Segments text into manageable chunks (*Content Chunking*).
- `purrfectmeow.WichienMaat` – Interprets query intent for precise results (*Semantic Search*).
- `purrfectmeow.KhaoManee` – Converts text to vectors and stores them (*Embedding & Storage*).
- `purrfectmeow.Malet` – Extracts data from PDFs, images, spreadsheets, and Markdown (*Text Extraction*).
- `purrfectmeow.Suphalaks` – Manages file operations and model/tokenizer loading (*Utility & Infrastructure*).

> **Note**: All modules are prefixed with `purrfectmeow` for namespace clarity and reflect Thai cat breed names.

## 🚀 Installation

PurrfectKit requires **Python 3.10 to 3.12.4**. We recommend using `uv` for fast dependency management, but `pip` works too.

### Using `uv` (Recommended)

```bash
git clone https://github.com/SUWALUTIONS/PurrfectKit.git
cd PurrfectKit
uv sync --extra-index-url https://download.pytorch.org/whl/cpu
```

### Using `pip`

```bash
git clone https://github.com/SUWALUTIONS/PurrfectKit.git
cd PurrfectKit
pip install . --extra-index-url https://download.pytorch.org/whl/cpu
```

The `--extra-index-url` ensures CPU-only PyTorch wheels are used for `torch`, `torchvision`, and `torchaudio`.

For development dependencies (e.g., `pytest`):

```bash
uv sync --extra-index-url https://download.pytorch.org/whl/cpu --extra dev
# or
pip install .[dev] --extra-index-url https://download.pytorch.org/whl/cpu
```

## 🐱 Quick Start

Extract text from a PDF and chunking using the `Malet` & `Kornja` module:

```python
from purrfectmeow import Malet, Kornja

file = "example/meowdy.pdf"
file_name = "meowdy.pdf"

with open("meowdy.pdf", "rb") as f:
    text = Malet.loader(f, "meowdy.pdf", loader="MARKITDOWN")

chunks = Kornja.chunking(
    text, 
    splitter="token",
    model_name="intfloat/multilingual-e5-large-instruct",
    chunk_size=200,
    chunk_overlap=10
)

```

Explore more examples in the Usage Guide.

## 🌟 Features

- **NLP**: Process text with `spacy`, `pythainlp`, and `transformers` for tasks like tokenization and semantic analysis.
- **OCR**: Extract text from images and PDFs using `surya-ocr`, `easyocr`, and `pytesseract`.
- **Document Processing**: Handle PDFs, images, and Markdown with `pymupdf` and `pdf2image`.
- **Multilingual Support**: Thai language processing via `pythainlp`, with extensibility for other languages.
- **AI & LLMs**: Leverage `torch` and `langchain-core` for retrieval-augmented generation (RAG) and embeddings.
- **Whimsical Design**: Thai cat breed-inspired module names for a fun developer experience.

## 📚 Documentation

- Usage Guide: Detailed examples for `Malet` and other modules.
- API Reference: Full documentation for all `purrfectmeow` modules.
- GitHub Repository: Source code and issue tracker.

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push and open a pull request.

See (CONTRIBUTING)[CONTRIBUTING] for details.

## 📄 License

PurrfectKit is released under the [MIT License](LICENSE).