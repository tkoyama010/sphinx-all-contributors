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

Using Emoji Icons
-----------------

The ``:emoji:`` option displays emoji icons before contribution types based on the all-contributors emoji key:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :emoji:

.. all-contributors:: ../.all-contributorsrc
   :emoji:

Combining Options
-----------------

You can combine both ``:profile:`` and ``:emoji:`` options:

.. code-block:: rst

    .. all-contributors:: ../.all-contributorsrc
       :profile:
       :emoji:

.. all-contributors:: ../.all-contributorsrc
   :profile:
   :emoji:

