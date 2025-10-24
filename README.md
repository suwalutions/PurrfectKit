![PurrfectMeow Logo](docs/_static/repo-logo.png)

# PurrfectKit

[![Docker Image](https://github.com/suwalutions/PurrfectKit/actions/workflows/docker-image.yml/badge.svg)](https://github.com/suwalutions/PurrfectKit/actions/workflows/docker-image.yml)

**PurrfectKit** is a toolkit that simplifies Retrieval-Augmented Generation (RAG) into 5 easy steps:
1. Suphalak - read content from files
2. Malet - split content into chunks
3. WichienMaat - embed chunks into vectors
4. KhaoManee - search vectors with queries
5. Kornja - generate answers from vectors

> **_NOTE:_** Each step is inspired by a unique Thai cat breed, making the workflow memorable and fun.

## Quickstart

### Prerequisites
- python
- tesseract
- git


### Installation
```bash
pip install git+https://github.com/suwalutions/PurrfectKit.git

```

### Usage
```python
from purrfectmeow.meow.felis import DocTemplate, MetaFile
from purrfectmeow import Suphalak, Malet, WichienMaat, KhaoManee

file_path = 'test/test.pdf'
metadata = MetaFile.get_metadata(file_path)
content = Suphalak.reading(open(file_path, 'rb').read(), 'test.pdf', loader='PYMUPDF')
chunks = Malet.chunking(content, chunk_method='token', chunk_size='500', chunk_overlap='25')
docs = DocTemplate.create_template(chunks, metadata)
embedding = WichienMaat.embedding(chunks)
query = WichienMaat.embedding("ทดสอบ")
KhaoManee.searching(query, embedding, docs, 2)

```

## 📄 License

PurrfectKit is released under the [MIT License](LICENSE).
