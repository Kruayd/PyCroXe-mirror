"""
===========================================================
Beam-on-target evaluated cross-sections provisionment layer
===========================================================

Private module for provisionment of evaluated cross-sections of beam-on-target
related processes.

Functions
---------

.. autosummary
    :toctree: generated/

    get_cross_sections_by_projectiles

"""

from collections.abc import Sequence as _Sequence

import numpy as _np
import xarray as _xr
from numpy.typing import NDArray as _NDArray
from numpy.typing import ArrayLike as _ArrayLike
from xarray import DataArray as _DataArray

from .._connection import CroXeConnection as _CroXeConnection
from ._query import SortKey as _SortKey
from ._query import BeamProcessRecord as _BeamProcessRecord
from ._query import BeamFitRecord as _BeamFitRecord
from . import _query, _evaluate

__all__: list[str] = ["get_cross_sections_by_projectiles"]


def get_cross_sections_by_projectiles(
    conn: _CroXeConnection,
    energies: _ArrayLike,
    initial_projectiles: list[str],
    target: str,
    product_frame: str = "projectile",
    sort_by: _Sequence[_SortKey] = ("year", "rms"),
) -> _DataArray:
    r"""
    Given a certain set of initial projectiles, retrieve all processes
    necessary to solve the problem of the evolution of the inital species,
    evaluate the cross-section for each process at each energy value in
    ``energies``. and finally return the evaluated cross-sections tensor in
    the form of a :py:class:`xarray.DataArray`.

    Parameters
    ----------
    conn : :py:class:`pycroxe.CroXeConnection`
        An open :py:class:`pycroxe.CroXeConnection`.
    energies : arraylike
        Energies in eV at which to evaluate the cross-sections. The provided
        arraylike is flattened out for convenience.
    inital_projectiles : list[str]
        List of chemical symbols of the starting projectile species.
    target : str
        Chemical symbol of the target species.
    product_frame : str, optional
        Reference frame of the product after the collision (default:
        ``'projectile'``).
    sort_by : Sequence[:py:data:`pycroxe.beam.SortKey`]
        Ordered sequence of :py:data:`pycroxe.beam.SortKey` values that
        determines the ``ORDER BY`` clause.  The first key is the primary sort
        criterion, the second (if present) is the tiebreaker, and so on.

    Returns
    -------
    cross_sections_tensor: :py:class:`xarray.DataArray`
        3-dimensional array of evaluated cross-sections with first dimension
        indexed by energy values, second dimension indexed by product species,
        and last dimension indexed by projectile species. Values where
        ``projectile == product`` represents total destruction processes
        cross-sections, hence they are negatively valued.

    Raises
    ------
    ValueError
        If ``inital_projectiles`` or ``sort_by`` are empty.

    Notes
    -----
    The structure of the returned :py:class:`xarray.DataArray` is such that it
    can be useful in solving problems of the like

    ..math:: \frac{d\Gamma_i}{dx} = n(x)\sigma_{ij}\Gamma_j\text{,}

    where :math:`\Gamma_i` and :math`\Gamma_j` are respectively the particle
    fluxes of the i-th product and the j-th species, while :math:`\sigma_{ij}`
    is the cross-section of the process that trasnforms the j-th projectile into
    the i-th product.
    """
    if not initial_projectiles:
        raise ValueError("initial_projectiles must contain at least one symbol.")

    if not sort_by:
        raise ValueError("sort_by must contain at least one SortKey.")

    energies_array: _NDArray[_np.float64] = _np.asarray(
        energies, dtype=_np.float64
    ).ravel()

    all_processes: list[_BeamProcessRecord] = (
        _query.get_descendant_processes_by_projectiles(
            conn, initial_projectiles, target, product_frame
        )
    )

    all_species_set = sorted(
        {s for p in all_processes for s in (p.projectile, p.product)}
    )

    all_species: _DataArray = _xr.DataArray(
        all_species_set,
        dims=("species"),
    )

    cross_sections_tensor: _DataArray = _xr.DataArray(
        _np.zeros(energies_array.shape + all_species.shape * 2, dtype=_np.float64),
        dims=["energy", "product", "projectile"],
        coords=[energies_array, all_species, all_species],
        name="Beam-on-target cross-sections",
        attrs={
            "cross-section units": "m²",
            "energy units": "eV",
            "target": target,
            "product frame": product_frame,
        },
    )

    for process in all_processes:
        fit_records: list[_BeamFitRecord] = _query.get_fits_by_process(
            conn,
            process.projectile,
            process.target,
            process.product,
            process.product_frame,
            sort_by,
        )
        cross_sections_tensor.loc[..., process.product, process.projectile] = (
            _evaluate.evaluate_fits(fit_records, energies_array)
        )

    cross_sections_tensor.loc[..., all_species, all_species] = _xr.where(
        cross_sections_tensor.loc[..., all_species, all_species] == 0,
        -1 * cross_sections_tensor.sum("product").loc[..., all_species],
        -1 * cross_sections_tensor.loc[..., all_species, all_species],
    )

    return cross_sections_tensor
