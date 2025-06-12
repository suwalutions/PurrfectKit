.. _dev-guide:

Developer Guide
===============

Welcome to the Developer Guide! This document provides step-by-step instructions
for contributing to the project. It covers issue creation, branching, development workflow,
and submitting pull requests.

Step 1: Create an Issue
-----------------------

Open a new issue with a concise, descriptive title and a detailed description of the bug,
feature, or improvement you propose. Use labels to categorize the issue
(e.g., ``bug``, ``enhancement``, ``documentation``).

Step 2: Create a Branch
-----------------------

Create a new branch for your work based on the issue number:

.. code-block:: bash

    git checkout -b fix-issue-<issue-number>

Replace ``<issue-number>`` with the relevant GitHub issue number.

Step 3: Implement Your Changes
------------------------------

Write your code following the project’s style and conventions. Include comments
and update documentation for any new functionality.

Step 4: Commit Your Changes
---------------------------

Stage and commit your changes with a clear, descriptive message:

.. code-block:: bash

    git add .
    git commit -m "Fixes #<issue-number>: Brief description of the fix"

Step 5: Push Your Branch
------------------------

Push your branch to your forked repository:

.. code-block:: bash

    git push origin fix-issue-<issue-number>

Step 6: Open a Pull Request
---------------------------

Open a Pull Request (PR) from your fork’s branch to the ``meow`` branch in the upstream repository.

- Reference the issue in your PR description (e.g., “Closes #<issue-number>”).
- Complete the PR template.
- Request a review from a maintainer.

Step 7: Address Feedback
------------------------

Respond to feedback from reviewers. Make any requested changes and push updates to your branch.

Step 8: Merge
-------------

After approval and successful checks, your PR will be merged into the ``meow`` branch.

.. note::
    If you need help at any step, feel free to reach out to the maintainers or ask in the project’s communication channels.
