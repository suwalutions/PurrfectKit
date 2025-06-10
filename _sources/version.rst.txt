.. _version:

📦 How to Release a New Version
================================

This guide outlines the steps for bumping the version, tagging a release, and optionally publishing the package to GitHub.


🚀 Steps to Release
====================

1. Ensure working directory is clean

    Make sure all your changes are committed::
        git status
        
        # There should be no uncommitted changes.

2. Bump the version

    Run the following command, replacing `patch` with `minor` or `major` as needed::
        make release part=patch

    This will:
    - Check for a clean Git working tree
    - Update the version in all relevant files (e.g., `pyproject.toml`, `__init__.py`, `uv.lock`)
    - Generate a changelog based on Git commit history
    - Commit and tag the new version
    - Push the commit and tag to GitHub

🛠 Bumping Examples
===================

+--------+-----------------------------+----------------------+
| Type   | Command                     | Effect               |
+========+=============================+======================+
| Patch  | ``make release part=patch`` | 0.1.2 → 0.1.3        |
+--------+-----------------------------+----------------------+
| Minor  | ``make release part=minor`` | 0.1.2 → 0.2.0        |
+--------+-----------------------------+----------------------+
| Major  | ``make release part=major`` | 0.1.2 → 1.0.0        |
+--------+-----------------------------+----------------------+

💡 Notes
=========

- The version is managed by `bumpversion`, and must match across all configured files.
- You can find the current version in `pyproject.toml` and `__init__.py`.
- The changelog is generated automatically from commit messages since the last tag.