.. include:: ../README.md
   :parser: myst_parser.sphinx_

Basic Usage
-----------

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc

.. all-contributors:: ../.all-contributorsrc

Using Profile Links
-------------------

The ``:profile:`` option makes contributor names clickable links to their profile URLs:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :profile:

.. all-contributors:: ../.all-contributorsrc
   :profile:

Using Table Format
------------------

The ``:table:`` option displays contributors in a table format instead of a bullet list:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :table:

.. all-contributors:: ../.all-contributorsrc
   :table:

Combining Options
-----------------

You can combine ``:table:`` and ``:profile:`` options to display contributors in a table with clickable profile links:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :table:
       :profile:

.. all-contributors:: ../.all-contributorsrc
   :table:
   :profile:
