Installation
============

Install via pip:

.. code-block:: console

    pip install purrfectkit


Install via git:

.. code-block:: console
  
    pip install -U git+https://github.com/suwalutions/PurrfectKit.git


Install from source:

.. code-block:: console

    git clone https://github.com/suwalutions/PurrfectKit.git
    pip installl -U PurrfectKit/.



Prerequisites
-------------

Before installing **PurrfectKit**, ensure the following dependencies are installed on your system.


.. _linux:

Linux (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~

**System Requirements**

- **Python**: Version **3.10** or higher
- **Tesseract OCR**: Required for OCR processing or image-based PDFs

  .. code-block:: console

      sudo apt-get install tesseract-ocr

- **Thai Tesseract** *(optional, for Thai text recognition)*

  .. code-block:: console

      sudo apt-get install tesseract-ocr-tha

- **Poppler**: Required for PDF to image conversion

  .. code-block:: console

      sudo apt-get install poppler-utils

- **FFmpeg**: Required for video/audio extraction and conversion

  .. code-block:: console

      sudo apt-get install ffmpeg

- **libmagic1**: Used for MIME-type detection

  .. code-block:: console

      sudo apt-get install libmagic1


.. _macos:

macOS
~~~~~

**System Requirements**

- **Python**: Version **3.10** or higher
- **Tesseract OCR**: Required for OCR processing or image-based PDFs

  .. code-block:: console

      brew install tesseract

- **Thai Tesseract** *(optional, for Thai text recognition)*

  .. code-block:: console

      brew install tesseract-lang

- **Poppler**: Required for PDF to image conversion

  .. code-block:: console

      brew install poppler

- **FFmpeg**: Required for video/audio extraction and conversion

  .. code-block:: console

      brew install ffmpeg

- **libmagic**: Used for MIME-type detection

  .. code-block:: console

      brew install libmagic

.. _windows:

.. note::

   For **Windows** users, it is recommended to install **Tesseract** and **Poppler** manually and ensure their executable paths are added to the system environment variables.
