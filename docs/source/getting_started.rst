===============
Getting started
===============

Installation
------------

At this development stage PyCroXe is not yet public on
`PyPI <https://pypi.org>`_, hence just running ``pip install pycroxe`` won't
make it. You can, though, clone the
`official Codeberg repo <https://codeberg.org/Kruayd/PyCroXe>`_ to your machine
and install PyCroXe from it:

.. code-block:: console

   git clone https://codeberg.org/Kruayd/PyCroXe.git
   pip install ./PyCroXe

Required dependencies
.....................

* Python (3.12 or later)
* `NumPy <https://numpy.org>`_ (1.26 or later)
* `xarray <https://docs.xarray.dev>`_ (2024.1 or later)
* `SQLAlchemy <https://www.sqlalchemy.org/>`_ (2.0 or later)
* `MariaDB <https://mariadb.com>`_ (11.1 or later)
* `MariaDB Connector for Python <https://mariadb.com/docs/connectors/connectors-quickstart-guides/connector-python-guide>`_
  (1.1 or later)
* A remote or local instance of `CroXe <https://codeberg.org/Kruayd/CroXe>`_

Usage
-----

tl;dr
.....

.. code-block:: python

   import numpy as np
   from pycroxe import connect, get_species_properties
   from pycroxe.beam import get_cross_sections_by_projectiles

   energies = np.geomspace(10, 1e5, 200) # energies in eV

   with connect() as conn:
       sigma = get_cross_sections_by_projectiles(
           conn,
           energies,
           initial_projectiles=["H3+", "H2+", "H+"],
           target="H2",
       )

       species_data = get_species_properties(
           conn,
           symbols=sigma.coords["product"].to_numpy().tolist(),
       )

But please, find some time to read the rest of the official docs!

Connecting
..........

PyCroXe provides a :py:func:`pycroxe.connect` function that can be used, as the
name obviously suggests, to connect to any network-reachable instance of CroXe.

The intended usage is within a ``with`` statement; this will make
:py:func:`pycroxe.connect`, if no argument is provided, return an instance of a
:py:class:`pycroxe.CroXeConnection` class, acting as a context manager, with an
open connection pointing towards the default URL
``mariadb+mariadbconnector://croxe-guest@localhost/CroXe``:

.. code-block:: python

   from pycroxe import connect

   with connect() as conn:
       ...

PyCroXe URLs follow the
`SQLAlchemy pattern <https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls>`_
(``dialect+driver://username@host:port/database``) and can be provided to the
:py:func:`pycroxe.connect` function, in order of descending precedence, by:

#. directly passing them as argument

   .. code-block:: python

      with connect(
          "mariadb+mariadbconnector://user@server.institute.org/CroXe"
      ) as conn:
          ...

#. setting up the environment variable ``CROXE_DB``

   .. code-block:: bash

      # if using bash
      export CROXE_DB="mysql+pymysql://user@server.institute.org/CroXe"

#. changing specific parts of the default URL with keyword arguments

   .. code-block:: python

      with connect(
          host="server.institute.org",
          user="user",
          connector="mariadb+mariadbconnector",
          database="CroXe_2_electric_boogaloo"
      ) as conn:
          ...

.. note::

   :py:func:`pycroxe.connect` can also be used outside ``with`` statements, but
   notice that this will return a closed instance of a
   :py:class:`pycroxe.CroXeConnection` class that must be opened and closed
   manually with the corresponding methods:

   .. code-block:: python

      from pycroxe import connect

      conn = connect()
      conn.open()
      ...
      conn.close()

   At this point, if you really wish not to use a ``with`` statement, you can
   just use the :py:class:`pycroxe.CroXeConnection` class instance builder, to
   which you can provide URLs in the same manner as to
   :py:func:`pycroxe.connect`:

   .. code-block:: python

      from pycroxe import CroXeConnection

      conn = CroXeConnection("mysql+pymysql://user@server.institute.org/CroXe")
      conn.open()
      ...
      conn.close()

.. caution::

   Using :py:func:`pycroxe.connect` and/or :py:class:`pycroxe.CroXeConnection`
   outside ``with`` statements is strongly discouraged!

Retrieving species properties
.............................

Function :py:func:`pycroxe.get_species_properties` will return a
`xarray Dataset <https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataset>`_
of properties of all the species stored in CroXe. If given the ``symbols``
keyword argument, data will be limited only to the chosen species:

.. code-block:: python

   from pycroxe import connect, get_species_properties

   with connect() as conn:
       species_data = get_species_properties(
           conn,
           symbols=["H+", "H2"],
       )

Retrieving beam-on-target processes cross-sections
..................................................

PyCroXe provides the :py:mod:`pycroxe.beam` module, which in turn provides the
:py:func:`pycroxe.beam.get_cross_sections_by_projectiles` function.
:py:func:`pycroxe.beam.get_cross_sections_by_projectiles` will first recursively
find all processes that may derive from the given list of initial projectile
species, and then return a 3D tensor of evaluated cross-sections, in the form
of a
`xarray DataArray <https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataarray>`_,
with first dimension indexing energy values, the second indexing product
species, and the last one indexing projectiles:

.. code-block:: python

   import numpy as np
   from pycroxe import connect
   from pycroxe.beam import get_cross_sections_by_projectiles

   energies = np.geomspace(10, 1e5, 200) # energies in eV

   with connect() as conn:
       sigma = get_cross_sections_by_projectiles(
           conn,
           energies,
           initial_projectiles=["H3+", "H2+", "H+"],
           target="H2",
       )
