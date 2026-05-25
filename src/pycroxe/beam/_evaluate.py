"""
====================================
Beam-on-target data evaluation layer
====================================

Private module for cross-section evaluation of beam-on-target related
processes.

Functions
---------

.. autosummary
    :toctree: generated/

    evaluate_fits

"""

import warnings as _warnings
import numpy as _np
from numpy.typing import NDArray as _NDArray

from ._query import BeamFitRecord as _BeamFitRecord
from ..fitfunctions import get_fit_function as _get_fit_function

__all__: list[str] = ["evaluate_fits"]


def evaluate_fits(
    fits: list[_BeamFitRecord],
    energies: _NDArray[_np.float64],
) -> _NDArray[_np.float64]:
    """
    Evaluate the cross-section of a beam-on-target process over ``energies``.

    For each energy value in ``energies``, this function will evaluate the
    cross-section of the process with the first fit whose domain
    ``[e_min, e_max]`` covers the energy value itself. Energy values not covered
    by any fit yield ``NaN``.


    Parameters
    ----------
    fits : list[:py:class:`pycroxe.beam.BeamFitRecord`]
        All available fits for a single beam-on-target process, sorted by
        decreasing preference.
    energies : ndarray
        Energies in eV at which to evaluate the cross-section.

    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as `energies`,
        in units of m².
    """
    result: _NDArray[_np.float64] = _np.full_like(energies, _np.nan)

    if not fits:
        _warnings.warn(
            "No fits were provided, possibly because one of the requested processes doesn't have any CroXe.beam_fit_params entry."
            " Returning an array full of NaNs",
            stacklevel=2,
        )
        return result

    pending: _NDArray[_np.bool_] = _np.ones(energies.shape, dtype=bool)

    for fit in fits:
        if not pending.any():
            break

        mask: _NDArray[_np.bool_] = (
            pending & (fit.e_min <= energies) & (energies <= fit.e_max)
        )

        if not mask.any():
            continue

        fit_function = _get_fit_function(fit.function_name)
        result[mask] = fit_function(energies[mask], fit.coefficients, **_build_ctx(fit))
        pending &= ~mask

    if _np.any(_np.isnan(result)):
        _warnings.warn(
            "Some energy values don't fall within any domain of the possible fits."
            " Returning an array with at least one NaN",
            stacklevel=2,
        )

    return result


# Private helpers
def _build_ctx(fit: _BeamFitRecord) -> dict[str, float]:
    """
    Build the context dictionary ``ctx`` with data provided by the given
    :py:class:`pycroxe.beam.BeamFitRecord`. ``ctx`` will be passed as
    ``**kwargs``, by :py:func:`pycroxe.beam.evaluate.evaluate_fits` to any
    registered fit function from :py:mod:`pycroxe.fitfunctions`.

    Parameters
    ----------
    fit : :py:class:`pycroxe.beam.BeamFitRecord`
        A record of the fit of any beam-on-target process.

    Returns
    -------
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.
    """
    return {
        "species_mass": fit.projectile_mass,
        "e_min": fit.e_min,
        "e_max": fit.e_max,
    }
