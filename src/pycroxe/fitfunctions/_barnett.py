"""
===========================
C. F. Barnett fit templates
===========================

This private module implements the fit function templates described and used by
C. F. Barnett.

Currently only the Chebyshev polynomial-based fit from [1]_ is implemented.

Functions
---------

.. autosummary::
   :toctree: generated/

   cheb

Notes
-----
Barnett expresses projectile energy in eV/amu and cross-sections in cm².
CroXe and this API store and accept energies in eV and cross-section in m². The
conversion is handled internally by each fit function.

Checking whether some energy value falls within the domain of some registered
function or not, is responsibility of the evaluation layer of each
:py:mod:`pycroxe` sub-module

References
----------
.. [1] C. F. Barnett, "Atomic Data for Fusion Volume 1: Collisions of H, H2, He
   and Li Atoms and Ions with Atoms and Molecules", *Controlled Fusion Atomic
   Data Center*, 1990 (https://doi.org/10.2172/6570226)
"""

import numpy as _np
from numpy.typing import ArrayLike as _ArrayLike
from numpy.typing import NDArray as _NDArray

__all__: list[str] = ["cheb"]

_CM2_TO_M2: float = 1e-4


def cheb(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Fit function template, based on a Chebyshev polynomial series, described
    and used by C. F. Barnett in [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Barnett's coefficients, in order of increasing degree, as stored in
        CroXe.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        Required keys:
            ``species_mass`` : float
                Atomic/molecular mass of the projectile in amu.
                Necessary for converting from eV to eV/amu.
            ``e_min`` : float
                Lower boundary of the fit domain in eV.
            ``e_max`` : float
                Upper boundary of the fit domain in eV.

    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as `energies`,
        in units of m².

    Raises
    ------
    KeyError
        If any among **species_mass**, **e_min**, or **e_max** is missing from
        ``ctx``.

    Notes
    -----
    The 0th-order coefficient of a Chebyshev polynomials series, ``C_0``,
    corresponds to half of Barnett's 0-th order coefficient, ``A_0``. Hence,
    ``C_0 = A_0 / 2``

    References
    ----------
    .. [1] C. F. Barnett, "Atomic Data for Fusion Volume 1: Collisions of H, H2, He
       and Li Atoms and Ions with Atoms and Molecules", *Controlled Fusion Atomic
       Data Center*, 1990 (https://doi.org/10.2172/6570226)
    """
    species_mass: float = ctx["species_mass"]
    e_min: float = ctx["e_min"]
    e_max: float = ctx["e_max"]

    energies = _np.asarray(energies, dtype=_np.float64)

    # Handle energy unit conversion
    e_amu = energies / species_mass

    # Barnett maps [log(e_min), log(e_max)] to the interval [-1, 1], where log
    # is the natural logarithm. Numpy's Chebyshev class can handle this mapping
    # with the additional keyword argument domain.
    domain = (
        _np.log(e_min / species_mass),
        _np.log(e_max / species_mass),
    )

    # Handle 0th-order coefficient conversion
    coeffs = _np.array(coefficients, dtype=_np.float64)
    coeffs[0] *= 0.5

    poly = _np.polynomial.Chebyshev(coeffs, domain=domain)
    return _np.exp(poly(_np.log(e_amu))) * _CM2_TO_M2
