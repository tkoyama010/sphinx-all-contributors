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

Using Avatar Icons
------------------

The ``:avatar:`` option displays contributor avatar/profile images from the ``avatar_url`` field:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :avatar:

.. all-contributors:: ../.all-contributorsrc
   :avatar:

Combining Options
-----------------

You can combine ``:table:``, ``:profile:``, and ``:avatar:`` options:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :table:
       :profile:

.. all-contributors:: ../.all-contributorsrc
   :table:
   :profile:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :profile:
       :avatar:

.. all-contributors:: ../.all-contributorsrc
   :profile:
   :avatar:
