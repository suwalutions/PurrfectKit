Quickstart
==========

Here are **5 easy steps** to build your RAG system with PurrfectKit.

.. code-block:: python

    from purrfectmeow.meow.felis import DocTemplate, MetaFile
    from purrfectmeow import Suphalak, Malet, WichienMaat, KhaoManee, Kornja

    # Step 1: Read content from a PDF
    file_path = 'test/test.pdf'
    with open(file_path, 'rb') as file:
        content = Suphalak.reading(file.read(), 'test.pdf', loader='PYMUPDF')

    # Step 2: Split content into chunks
    chunks = Malet.chunking(content, chunk_method='token', chunk_size=500, chunk_overlap=25)

    # Step 3: Create document template with metadata
    metadata = MetaFile.get_metadata(file_path)
    docs = DocTemplate.create_template(chunks, metadata)

    # Step 4: Embed chunks and query
    chunk_embeddings = WichienMaat.embedding(chunks)
    query = "What is the main topic of the document?"
    query_embedding = WichienMaat.embedding(query)

    # Step 5: Search for relevant chunks
    results = KhaoManee.searching(query_embedding, chunk_embeddings, docs, top_k=2)

    # (Optional) Step 6: Generate answer (if implemented)
    # answer = Kornja.generating(results, query)
    # print(answer)

    print("Top search results:", results)

This example reads a PDF, chunks it, embeds the chunks, searches for relevant content, and (if implemented) generates an answer.