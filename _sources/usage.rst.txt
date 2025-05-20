Usage
=====

The :class:`purrfectmeow.Malet` class provides a versatile :meth:`loader` method to process files in various formats. Below are examples demonstrating its capabilities, grouped by loader type.

Available Loaders Options
-------------------------

The :meth:`purrfectmeow.Malet.loader` method supports the following loaders:

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: longtable

   * - Loader
     - Description
   * - :const:`MARKITDOWN`
     - Converts content to Markdown using the MarkItDown library.
   * - :const:`DOCLING`
     - Converts content to Markdown using the Docling library.
   * - :const:`PYTESSERACT`
     - Performs OCR on images or PDFs using Tesseract.
   * - :const:`EASYOCR`
     - Performs OCR on images or PDFs using EasyOCR.
   * - :const:`SURYAOCR`
     - Performs OCR on images or PDFs using SuryaOCR.
   * - :const:`PYMUPDF`
     - Extracts text from PDFs using PyMuPDF.
   * - :const:`PYMUPDF_AS_TXT`
     - Extracts plain text from PDFs using PyMuPDF.
   * - :const:`PANDAS_EXCEL`
     - Reads Excel files into text or data structures using pandas.
   * - :const:`PANDAS_CSV`
     - Reads CSV files into text or data structures using pandas.

Simple Loaders
-------------------

Extract text or data from files using straightforward loaders like :const:`PYMUPDF` or :const:`PANDAS_EXCEL`.

.. code-block:: python

   from purrfectmeow import Malet

   # Extract text from a PDF using PyMuPDF
   try:
       docs = Malet.loader("example.pdf", "example.pdf", loader="PYMUPDF")
       print("Extracted PDF text:", docs[:200])  # Print first 200 characters
   except FileNotFoundError:
       print("Error: File 'example.pdf' not found.")
   except ValueError as e:
       print(f"Error: {e}")

   # Extract data from an Excel file using pandas
   try:
       docs = Malet.loader("data.xlsx", "data.xlsx", loader="PANDAS_EXCEL")
       print("Excel data:", docs.head() if hasattr(docs, "head") else docs)
   except FileNotFoundError:
       print("Error: File 'data.xlsx' not found.")
   except ValueError as e:
       print(f"Error: {e}")

OCR Loaders
-----------

Use OCR loaders to extract text from images or scanned PDFs.

.. code-block:: python

   from purrfectmeow import Malet

   # Perform OCR on an image using EasyOCR
   try:
       with open("scanned_image.png", "rb") as f:
           text = Malet.loader(f, "scanned_image.png", loader="EASYOCR")
           print("OCR text:", text[:200])  # Print first 200 characters
   except FileNotFoundError:
       print("Error: File 'scanned_image.png' not found.")
   except ValueError as e:
       print(f"Error: {e}")

   # Perform OCR on a receipt image using SuryaOCR
   try:
       with open("receipt.jpg", "rb") as f:
           text = Malet.loader(f, "receipt.jpg", loader="SURYAOCR")
           print("OCR text:", text[:200])  # Print first 200 characters
   except FileNotFoundError:
       print("Error: File 'receipt.jpg' not found.")
   except ValueError as e:
       print(f"Error: {e}")

Markdown Loaders
----------------

Convert files to Markdown format for structured text output.

.. code-block:: python

   from purrfectmeow import Malet

   # Convert a file to Markdown using MarkItDown
   try:
       docs = Malet.loader("notes.md", "notes.md", loader="MARKITDOWN")
       print("Markdown output:", docs[:200])  # Print first 200 characters
   except FileNotFoundError:
       print("Error: File 'notes.md' not found.")
   except ValueError as e:
       print(f"Error: {e}")

   # Convert a file to Markdown using Docling
   try:
       docs = Malet.loader("document.md", "document.md", loader="DOCLING")
       print("Markdown output:", docs[:200])  # Print first 200 characters
   except FileNotFoundError:
       print("Error: File 'document.md' not found.")
   except ValueError as e:
       print(f"Error: {e}")
