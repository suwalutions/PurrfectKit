.. PurrfectKit documentation master file, created by
   sphinx-quickstart on Fri Oct 24 11:38:46 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PurrfectKit's documentation
===========================

.. image:: /_static/repo-logo.png

**PurrfectKit** (/purr-fekt-kit/) is a Python library for effortless Retrieval-Augmented Generation (RAG) workflows.

.. image:: https://img.shields.io/badge/python-3.10–3.13-blue
   :target: https://www.python.org

.. image:: https://img.shields.io/pypi/v/purrfectkit?color=gold&label=PyPI 
   :target: https://pypi.org/project/purrfectkit/

.. image:: https://img.shields.io/pypi/dm/purrfectkit?color=purple
   :target: https://pypistats.org/packages/purrfectkit

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff

.. image:: https://img.shields.io/docker/v/suwalutions/purrfectkit?label=docker
   :target: https://ghcr.io/suwalutions/purrfectkit

.. image:: https://codecov.io/github/suwalutions/PurrfectKit/branch/meow/graph/badge.svg?token=Z6YETHJXCL 
   :target: https://codecov.io/github/suwalutions/PurrfectKit
 
.. note::

   This project is under active development.

**PurrfectKit** simplifies Retrieval-Augmented Generation (RAG), a technique combining information retrieval and text generation to answer queries using external documents. 

The workflow involves five steps, each named after a Thai cat breed for a memorable experience:

1. :ref:`Suphalak <suphalak>`: Extract text from files (e.g., PDFs).
2. :ref:`Malet <malet>`: Split text into manageable chunks.
3. :ref:`WichienMaat <wichienmaat>`: Convert chunks into numerical embeddings for search.
4. :ref:`KhaoManee <khaomanee>`: Search for chunks relevant to a query.
5. :ref:`Kornja <kornja>`: Generate answers using retrieved chunks (under development).

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   usage
   modules
   contributing
