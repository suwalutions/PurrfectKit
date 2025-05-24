Usage
=====

🐱 Quick Start
--------------

Extract text from a PDF and chunking using the ``Malet`` & ``Kornja`` module:

.. code-block:: python

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

Expected Output
---------------

.. code-block:: json

    [
        {
            "score": 0.814572274684906,
            "document": "<Document with metadata and content>"
        },
        {
            "score": 0.8024211525917053,
            "document": "<Document with metadata and content>"
        }
    ]

.. code-block:: text

    Document(
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