.. _readme:

PurrfectKit
===========

PurrfectKit is a whimsical Python library that blends feline charm with powerful NLP functionality. Inspired by Thai cat breeds, each module in the :mod:`purrfectmeow` package maps to a specific NLP technique, making text processing both fun and efficient.

Overview
----------------

PurrfectKit's core modules, each inspired by a Thai cat breed:

- :class:`purrfectmeow.Kornja`: Breaks text into manageable segments (Content Chunking).
- :class:`purrfectmeow.WichienMaat`: Understands query intent for precise results (Semantic Search).
- :class:`purrfectmeow.KhaoManee`: Converts text to vectors and stores them (Embedding & Storage).
- :class:`purrfectmeow.Malet`: Extracts data from PDFs, images, spreadsheets, and Markdown (Text Extraction).
- :class:`purrfectmeow.Suphalaks`: Provides internal utilities for seamless operation.

.. note::
   Module names reflect Thai cat breeds, prefixed with ``purrfectmeow`` for namespace clarity.

Installation
------------

Ensure Python 3.10 or higher is installed, then clone and install PurrfectKit:

.. code-block:: console

   $ git clone https://github.com/suwalutions/PurrfectKit.git
   $ cd PurrfectKit
   $ pip install -e .

Quick Start
-----------

Try extracting text from a PDF using the :class:`purrfectmeow.Malet` class:

.. code-block:: python

   from purrfectmeow import Malet

   try:
       docs = Malet.loader("example.pdf", "example.pdf", loader="PYMUPDF")
       print("Extracted text:", docs[:200])
   except FileNotFoundError:
       print("Error: File 'example.pdf' not found.")
   except ValueError as e:
       print(f"Error: {e}")

See :doc:`usage` for more examples.

Documentation
-------------

- :doc:`usage`: Detailed examples for :class:`purrfectmeow.Malet`.
- :doc:`api`: API reference for all modules.

License
-------

PurrfectKit is released under the license in the `LICENSE <https://github.com/suwalutions/PurrfectKit/blob/main/LICENSE>`_ file.
