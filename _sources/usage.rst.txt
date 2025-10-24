Usage
=====

**PurrfectKit** simplifies Retrieval-Augmented Generation (RAG), a technique combining information retrieval and text generation to answer queries using external documents. 

The workflow involves five steps, each named after a Thai cat breed for a memorable experience:

1. **Suphalak**: Extract text from files (e.g., PDFs).
2. **Malet**: Split text into manageable chunks.
3. **WichienMaat**: Convert chunks into numerical embeddings for search.
4. **KhaoManee**: Search for chunks relevant to a query.
5. **Kornja**: Generate answers using retrieved chunks (under development).

Suphalak
--------

Read content from files

.. py:function:: Suphalak.reading(file, file_name, loader)

    Extract and return the content of a file as a string.

    :param file: The file object to read.
    :type file: BinaryIO
    :param file_name: The name of the file.
    :type file_name: str
    :param loader: The loader type used for parsing.
    :type loader: str
    :return: Extracted content from the file.
    :rtype: str

Malet
-----

Split content into chunks

.. py:function:: Malet.chunking(text, chunk_method="token", **kwargs)

    Split text into chunks using the specified method.

    :param text: The text to split.
    :type text: str
    :param chunk_method: The method for chunking ("token" or "separate").
    :type chunk_method: Optional[Literal["token", "separate"]]
    :param `**kwargs`: Additional parameters for chunking.
    :type `**kwargs`: Any
    :return: List of text chunks.
    :rtype: list[str]

WichienMaat
-----------

Embed chunks into vectors

.. py:function:: WichienMaat.embedding(sentence, model_name=None)

    Convert sentences into vector embeddings.

    :param sentence: A single sentence or a list of sentences.
    :type sentence: str | list[str]
    :param model_name: Optional model name for embedding.
    :type model_name: Optional[str]
    :return: Embedding vectors as a NumPy array.
    :rtype: numpy.ndarray

KhaoManee
---------

Search vectors with queries

.. py:function:: KhaoManee.searching(query_embed, sentence_embed, document, top_k)

    Search for the most relevant chunks based on query embeddings.

    :param query_embed: Query embedding vector.
    :type query_embed: numpy.ndarray
    :param sentence_embed: Embeddings of sentences to search.
    :type sentence_embed: numpy.ndarray
    :param document: The original document object.
    :type document: Document
    :param top_k: Number of top results to return.
    :type top_k: int
    :return: List of search results with relevance scores.
    :rtype: list[dict]

Kornja
------

Generate answers from vectors

.. py:function:: Kornja.generating()

    .. note:: This function is under development and will generate answers from retrieved contexts in future releases.
        
.. .. py:function:: Kornja.generating(context, query, **kwargs)

..     Generate an answer based on retrieved vector context.

..     :param context: Retrieved context for generating answer.
..     :type context: list[dict]
..     :param query: The user query.
..     :type query: str
..     :param `**kwargs`: Additional parameters for generation.
..     :type `**kwargs`: Any
..     :return: Generated answer string.
..     :rtype: str
