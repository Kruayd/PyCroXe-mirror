r"""
========================
Beam-on-target processes
========================

This module contains data classes, queries and functions related to processes
of the kind::

    projectile + target -> product

Corresponding database tables:

* ``beam_processes``
* ``beam_fit_params``
* ``beam_fit_coefficients``

Data classes
------------

.. autosummary::
    :toctree: generated/

    BeamProcessRecord
    BeamFitRecord

Database queries
----------------

.. autosummary::
    :toctree: generated/

    get_processes
    get_descendant_processes_by_projectiles
    get_fits_by_process

Cross-sections retrieval
------------------------

.. autosummary
    :toctree: generated/

    get_cross_sections_by_projectiles

Types
-----

.. autosummary::
    :toctree: generated/

    SortKey

Usage
-----
If you are trying to solve problems of the like

.. math:: \frac{d\Gamma_i}{dx}=n(x)\sigma_{ij}\Gamma_j\text{,}
    :label: eq_part_flux

either analytically or numerically, your go-to function is
:py:func:`pycroxe.beam.get_cross_sections_by_projectiles`, which will retrieve
the cross-sections of all the necessary processes to solve your problem, given
the initial conditions of the starting projectile species and their energies.

Alternatively, you can get direct access to database queries with functions from
section `Database queries`_.

You also get access to `classes <Data classes_>`_ and `type aliases <Types_>`_
for type hinting in your code.

Notes
-----
In equation :eq:`eq_part_flux` :math:`\Gamma_i` and :math:`\Gamma_j` are
respectively the particle fluxes of the i-th product and the j-th species,
while :math:`\sigma_{ij}` is the cross-section of the process that trasnforms
the j-th projectile into the i-th product.
:py:func:`pycroxe.beam.get_cross_sections_by_projectiles` returns a
3-dimensional version of the :math:`\sigma_{ij}` tensor, where the extra
dimension, set as the first index of the array, represents the provided energy
values.

CroXe and this API store and accept energies in eV and cross-section in m². In
the case of authors using different units of measurments (usually cm² for
cross-sections, and eV/amu or keV for energies), the conversion is handled
internally by each fit function registered in :py:mod:`pycroxe.fitfunctions`.
"""

from ._query import (
    BeamProcessRecord,
    BeamFitRecord,
    SortKey,
    get_processes,
    get_descendant_processes_by_projectiles,
    get_fits_by_process,
)

from ._api import get_cross_sections_by_projectiles

__all__: list[str] = [
    "BeamProcessRecord",
    "BeamFitRecord",
    "SortKey",
    "get_processes",
    "get_descendant_processes_by_projectiles",
    "get_fits_by_process",
    "get_cross_sections_by_projectiles",
]
