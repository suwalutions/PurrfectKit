![PurrfectMeow Logo](https://github.com/suwalutions/PurrfectKit/blob/meow/docs/_static/repo-logo.png)

# PurrfectKit

[![PyPI Latest Release](https://img.shields.io/pypi/v/purrfectkit.svg)](https://pypi.org/project/purrfectkit/) [![PyPI Downloads](https://img.shields.io/pypi/dm/purrfectkit.svg?label=PyPI%20downloads)](https://pypi.org/project/purrfectkit/)
[![Docker Image](https://github.com/suwalutions/PurrfectKit/actions/workflows/docker-image.yml/badge.svg)](https://github.com/suwalutions/PurrfectKit/actions/workflows/docker-image.yml)
[![License - MIT](https://img.shields.io/pypi/l/purrfectkit.svg)](https://github.com/suwalutions/purrfectkit/blob/meow/LICENSE)

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

## 📄 License

PurrfectKit is released under the [MIT License](LICENSE).
