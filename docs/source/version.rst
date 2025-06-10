.. _version:

Versioning
==========

This guide outlines the process for bumping the version, generating a changelog, tagging a release, and pushing it to GitHub.

🚀 Steps to Release
--------------------

1. **Ensure a clean working tree**

Before releasing, make sure your working directory is clean—no uncommitted or staged changes.

.. code-block:: bash

    git status

.. note::

    The working tree and index must be clean. See `CONTRIBUTING <../../../CONTRIBUTING.md>`_ for detailed guidelines.

2. **Bump the version and release**

Use the `make release` command with the appropriate version part (`patch`, `minor`, or `major`).

.. code-block:: bash

    make release v-part=patch

This command will:

1. Ensure the Git working directory is clean
2. Update the version in all relevant files (`pyproject.toml`, `uv.lock`, `__init__.py`)
3. Generate a changelog based on commit history since the last tag
4. Commit all changes and tag the new version
5. Push the commit and tag to GitHub

🛠 Bumping Examples
-------------------

+--------+-------------------------------+----------------------+-----------------------------+
| Type   | Command                       | Resulting Version    | Description                 |
+========+===============================+======================+=============================+
| Patch  | ``make release v-part=patch`` | 0.1.2 → 0.1.3        | Fixes or small changes      |
+--------+-------------------------------+----------------------+-----------------------------+
| Minor  | ``make release v-part=minor`` | 0.1.2 → 0.2.0        | New features, no breaking   |
+--------+-------------------------------+----------------------+-----------------------------+
| Major  | ``make release v-part=major`` | 0.1.2 → 1.0.0        | Breaking changes            |
+--------+-------------------------------+----------------------+-----------------------------+

💡 Notes
---------

- Versioning is handled by `bumpversion` (or `bump2version`) and updates all configured files.
- The current version is typically found in `pyproject.toml`, `__init__.py`, and optionally `uv.lock`.
- The changelog is generated automatically using recent Git commit messages since the last tag.
- It's a good practice to write meaningful commit messages, especially if they follow Conventional Commits, to improve changelog quality.
