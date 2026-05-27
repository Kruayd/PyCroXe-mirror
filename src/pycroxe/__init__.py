"""
========
pycroxe
========

Python API for CroXe: a relational database of cross-sections and rate
coefficients for atomic processes and alike. If you are lookig for the database
itself, see `CroXe <https://codeberg.org/Kruayd/CroXe>`_.

Sub-modules
-----------

.. autosummary::
    :toctree: generated/

    beam
    fitfunctions

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
The recommended entry point for most use cases::

    import numpy as np
    from pycroxe import connect, get_species_properties
    from pycroxe.beam import get_cross_sections_by_projectiles

    energies = np.geomspace(10, 1e5, 200)  # eV

    with connect() as conn:
        sigma = get_cross_sections_by_projectiles(
            conn,
            energies,
            initial_projectiles=["H3+", "H2+", "H+"],
            target="H2",
        )

        species_data = get_species_properties(
            conn,
            sigma.coords["product"].to_numpy().tolist(),
        )

See :py:mod:`pycroxe.beam` for full documentation of available queries and
cross-section retrieval, and :py:mod:`pycroxe.fitfunctions` for the fit
function registry.

Notes
-----
CroXe is hosted as a MariaDB database. By default :py:func:`pycroxe.connect`
connects to ``localhost`` as ``croxe-guest``. Override via the ``CROXE_DB``
environment variable or by passing an explicit URL::

    with connect("mariadb+mariadbconnector://user@server.institute.org/CroXe") as conn:
        ...

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
