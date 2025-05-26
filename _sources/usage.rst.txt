.. _usage:

Usage Guide
===========

Welcome to the **PurrfectKit** usage guide! This document walks you through basic and advanced functionality using the Thai-cat-inspired `purrfectmeow` modules. From loading files to performing semantic search, you'll learn how to orchestrate your document intelligence pipeline with elegance and ease.

🚀 Getting Started
-------------------

To begin using PurrfectKit, ensure you've followed the installation steps in the README.

🗂️ File Metadata Extraction
----------------------------

Use ``Suphalaks.get_file_metadata`` to retrieve detailed metadata from a supported file:

.. code-block:: python

    from purrfectmeow import Suphalaks

    file_path = "example/meowdy.pdf"
    metadata = Suphalaks.get_file_metadata(file_path)

    print(metadata)

📝 Text Extraction
-------------------

Extract text from PDFs, Markdown, or images using the ``Malet.loader`` function:

.. code-block:: python

    from purrfectmeow import Malet

    with open(file_path, "rb") as f:
        text = Malet.loader(f, file_path, loader="MARKITDOWN")

    print(text[:300])  # Print first 300 characters

✂️ Chunking Text
-----------------

Split the raw text into meaningful chunks with ``Kornja.chunking``. This improves performance for downstream tasks like embedding and search.

.. code-block:: python
    
    from purrfectmeow import Kornja

    chunks = Kornja.chunking(
        text,
        splitter="token",
        model_name="intfloat/multilingual-e5-large-instruct",
        chunk_size=50,
        chunk_overlap=10
    )

    print(f"Number of chunks: {len(chunks)}")

🧾 Document Templating
-----------------------

Wrap the chunks into a document template for embedding and search:

.. code-block:: python

   docs = Suphalaks.document_template(chunks, metadata)

🧠 Embeddings
--------------

Generate embeddings for both your documents and queries with ``KhaoManee``:

.. code-block:: python

    from purrfectmeow import KhaoManee

    # Embed documents
    doc_embeddings = KhaoManee.get_embeddings(
        docs,
        model_name="intfloat/multilingual-e5-large-instruct"
    )

    # Embed a query
    query_embeddings = KhaoManee.get_query_embeddings(
        query="Where is the best cat café?",
        model_name="intfloat/multilingual-e5-large-instruct"
    )

🔍 Semantic Search
-------------------

Find the most relevant documents using ``WichienMaat.get_search``:

.. code-block:: python

    from purrfectmeow import WichienMaat

    results = WichienMaat.get_search(
        query_embeddings=query_embeddings,
        doc_embeddings=doc_embeddings,
        docs=docs,
        top_k=3
    )

    for result in results:
        print(f"Score: {result['score']:.4f}")
        print(f"Content: {result['document'].page_content[:200]}\n")

🖼️ Working with Other File Types
---------------------------------

PurrfectKit supports various file formats out-of-the-box. Examples:

- Markdown: ``loader="MARKITDOWN"``
- PDF: ``loader="PYMUPDF"``, or ``loader="EASYOCR"``
- Image: ``loader="PYTESSERACT"``, or ``loader="SURYAOCR"``

Example for image OCR:

.. code-block:: python

   image_path = "example/catnote.jpg"
   with open(image_path, "rb") as f:
       text = Malet.loader(f, image_path)

   print(text)

🧬 Advanced Use: Custom Models
-------------------------------

You can use your own embedding model if it supports HuggingFace-compatible API:

.. code-block:: python

   embeddings = KhaoManee.get_embeddings(
       docs,
       model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
   )

💡 Notes & Tips
----------------

- Use ``chunk_overlap > 0`` to preserve context between text chunks.
- The `loader` argument in ``Malet.loader`` determines which backend parser is used.
- Thai text support is best with ``pythainlp`` installed and Tesseract's Thai data.
- Explore `purrfectmeow.suphalaks` for file utilities like hashing, extension checks, and format detection.

For deeper exploration, see the full API Reference and test scripts under the ``examples/`` and ``tests/`` directories of the repository.
