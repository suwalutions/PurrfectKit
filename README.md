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
from purrfectmeow import Suphalaks, Malet, Kornja, KhaoManee

file = "example/meowdy.pdf"
file_name = "meowdy.pdf"

metadata = Suphalaks.get_file_metadata(file)

with open("meowdy.pdf", "rb") as f:
    text = Malet.loader(f, "meowdy.pdf", loader="MARKITDOWN")

chunks = Kornja.chunking(
    text, 
    splitter="token",
    model_name="intfloat/multilingual-e5-large-instruct",
    chunk_size=50,
    chunk_overlap=0
)

docs = Suphalaks.get_document_template(chunks, metadata)

embeddings = KhaoManee.get_embeddings(docs, model_name)
query_embeddings = KhaoManee.get_query_embeddings(query="howdy", model_name=model_name)

results = KhaoManee.get_search(query_embeddings, embeddings, docs, 2)

```
### Expected Output
```json
[
    {
    "score": 0.814572274684906,
    "document": Document(
        metadata={
            "chunk_info": {
                "chunk_number": 1, 
                "chunk_id": "fc690110e8a2407db6b65e7129331ec7", 
                "chunk_hash": "4b7ffc7f57494fba188f7bc55d348a7c", 
                "previous_chunk_hash": None, 
                "next_chunk_hash": "49473745424e819315a4ad8cb2c25fa8", 
                "chunk_size": 168
            }, "source_info": {
                "file_name": "meowdy.pdf", 
                "file_size": 3981724, 
                "file_created_date": "2025-05-23 09:46:17", 
                "file_modified_date": "2025-05-23 09:46:17", 
                "file_extension": ".pdf", 
                "file_type": "application/pdf", 
                "description": "PDF document, version 1.7, 1 pages", 
                "total_pages": 1, 
                "file_md5": "bf4db19df52cb3a3e4e3854c9edbdc73"
            }
        }, 
        page_content="   Meowdy, marvelous makers of machine magic!    \n \n  PurrfectKit. Whether you're chunking, searching, embedding, extracting, or orchestrating, \nI've got a cat for that"
    )
    },
    {
    "score": 0.8024211525917053,
    "document": Document(
        metadata={
            "chunk_info": {
                "chunk_number": 8, 
                "chunk_id": "ead74e45027442e58b4cc7af40f6770b", 
                "chunk_hash": "45b2c9bd82395c4c2179d4700ae72e22", 
                "previous_chunk_hash": "e41bf2dd4814ac8ef10492374503a4e3", 
                "next_chunk_hash": None, 
                "chunk_size": 95
            }, 
            "source_info": {
                "file_name": "meowdy.pdf", 
                "file_size": 3981724, 
                "file_created_date": "2025-05-23 09:46:17", 
                "file_modified_date": "2025-05-23 09:46:17", 
                "file_extension": ".pdf", 
                "file_type": "application/pdf", 
                "description": "PDF document, version 1.7, 1 pages", 
                "total_pages": 1, 
                "file_md5": "bf4db19df52cb3a3e4e3854c9edbdc73"
            }
        }, page_content=" wonder, your loyal library, \n  PurrfectKit \n \n  Star us on GitHub if we make your tails wag! \n"
    )
    },
]
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