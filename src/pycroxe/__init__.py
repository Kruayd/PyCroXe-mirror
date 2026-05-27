"""
========
PyCroXe
========

Python API for CroXe: a relational database of cross-sections and rate
coefficients for atomic processes and alike. If you are lookig for the database
itself, see `CroXe <https://codeberg.org/Kruayd/CroXe>`_.

Classes
-------

.. autosummary::
    :toctree: generated/

    CroXeConnection

Functions
---------

.. autosummary::
    :toctree: generated/

    connect

Generic data retrieval
----------------------

.. autosummary::
    :toctree: generated/

    get_species_properties

Usage
-----
This root module provides, through the function :py:func:`pycroxe.connect` and
the class :py:class:`pycroxe.CroXeConnection`, the basic interface to manage
connections with any instance of CroXe.

While :py:class:`pycroxe.CroXeConnection` is provided mainly for type hinting,
the recommended usage of :py:func:`pycroxe.connect` is within a ``with``
statement::

    from pycroxe import connect

    with connect() as conn:
        ...

which will return a :py:class:`pycroxe.CroXeConnection` instance acting as a
context manager (i.e. will take care of opening and closing connections
automatically).

You can change the default connection URL
(``mariadb+mariadbconnector://croxe-guest@localhost/CroXe``) by, in order of
decreasing precedence:

#. passing a valid URL as an argument to :py:func:`pycroxe.connect`
#. setting the environment variable ``CROXE_DB`` to a valid URL
#. changing specific parts of the default URL with :py:func:`pycroxe.connect`
   keyword arguments

You get also access to some
`generic data retrieval functions <Generic data retrieval_>`_, such as
:py:func:`pycroxe.get_species_properties`.

See :py:mod:`pycroxe.beam` for full documentation of more specialized queries
and cross-section retrieval, and :py:mod:`pycroxe.fitfunctions` for the fit
function registry.

Notes
-----
PyCroXe URLs follow the
`SQLAlchemy pattern <https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls>`_
(``dialect+driver://username@host:port/database``)

It is also possible, but not advisable, to get direct access to the
:py:class:`pycroxe.CroXeConnection` class. In this case, the caller will be
responsible for closing the connection::

    from pycroxe import CroXeConnection

    conn = CroXeConnection()
    conn.open()
    ...
    conn.close()
"""

from ._connection import CroXeConnection, connect

from ._api import get_species_properties

from . import beam, fitfunctions

__all__: list[str] = [
    "CroXeConnection",
    "connect",
    "get_species_properties",
    "beam",
    "fitfunctions",
]
