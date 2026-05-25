"""
===========================
T. Tabata fit templates
===========================

This private module implements the fit function templates described and used by
T. Tabata.

Currently only fit functions from [1]_ are implemented.

Functions
---------

.. autosummary::
   :toctree: generated/

   tab2_1_1
   tab2_1_2
   tab2_1_3
   tab2_1_4
   tab2_1_5
   tab2_1_6
   tab2_1_7
   tab2_1_8
   tab2_1_9
   tab2_1_10
   tab2_1_11
   tab2_1_12
   tab2_1_13
   tab2_1_14

Notes
-----
Public functions in this module are named with a leading triad of numbers
assigned in such a way that the first number indicates in which volume of the
"*Atomic and Molecular Collision Cross Sections*" the function appears, the
second number corresponds to the n-th paper within the volume, and the last one
is the label assigned by Tabata himself to the function, within the paper.
Following this convention, function ``tab2_1_4`` is, hence, function 4 in the
first paper of "*Atomic and Molecular Collision Cross Sections (2)*".

Tabata builds every fit function template, referred by him as *analytic
expressions*, as a linear combination of four fundamental functions, referred by
him as *basic relations* _[1]. These basic relations, which are not publicly
available, are used for the sole purpose of implementing Tabata's analytic
expressions.

Tabata expresses projectile and threshold energies in keV, while cross-section
is expressed in cm². CroXe and this API store and accept energies in eV and
cross-section in m². The conversion is handled internally by each fit function.

Checking whether some energy value falls within the domain of some registered
function or not, is responsibility of the evaluation layer of each
:py:mod:`pycroxe` sub-module

References
----------
.. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic and
   Molecular Collision Cross Sections (2)", *IDEA*, 2018
   (https://doi.org/10.13140/RG.2.2.26689.07521)
"""

import numpy as _np
from numpy.typing import ArrayLike as _ArrayLike
from numpy.typing import NDArray as _NDArray

__all__: list[str] = [
    "tab2_1_1",
    "tab2_1_2",
    "tab2_1_3",
    "tab2_1_4",
    "tab2_1_5",
    "tab2_1_6",
    "tab2_1_7",
    "tab2_1_8",
    "tab2_1_9",
    "tab2_1_10",
    "tab2_1_11",
    "tab2_1_12",
    "tab2_1_13",
    "tab2_1_14",
]

_EV_TO_KEV: float = 1e-3
_CM2_TO_M2: float = 1e-4

# Rydberg energy in keV (using Tabata's value)
_RY_KEV: float = 13.61e-3

# Tabata's σ0 constant (in cm²)
_SIGMA0_CM2: float = 1e-16


# Tabata's basic relations. These are private functions
def _basic_i(
    d: _NDArray[_np.float64],
    c1: float,
    c2: float,
) -> _NDArray[_np.float64]:
    """
    Tabata's first basic relation, as described in [1]_.

    Parameters
    ----------
    d : ndarray
        Differences in keV between energies and threshold energy. Must be
        non-negative for real-valued results.
    c1 : float
        First coefficient of the basic relation.
    c2 : float
        Second coefficient of the basic relation.

    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``d``, in
        units of cm².

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    return _SIGMA0_CM2 * c1 * (d / _RY_KEV) ** c2


def _basic_ii(
    d: _NDArray[_np.float64],
    c1: float,
    c2: float,
    c3: float,
    c4: float,
) -> _NDArray[_np.float64]:
    """
    Tabata's second basic relation, as described in [1]_.

    Parameters
    ----------
    d : ndarray
        Differences in keV between energies and threshold energy. Must be
        non-negative for real-valued results.
    c1 : float
        First coefficient of the basic relation.
    c2 : float
        Second coefficient of the basic relation.
    c3 : float
        Third coefficient of the basic relation.
    c4 : float
        Fourth coefficient of the basic relation.

    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``d``, in
        units of cm².

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    return _basic_i(d, c1, c2) / (1.0 + (d / c3) ** (c2 + c4))


def _basic_iii(
    d: _NDArray[_np.float64],
    c1: float,
    c2: float,
    c3: float,
    c4: float,
    c5: float,
    c6: float,
) -> _NDArray[_np.float64]:
    """
    Tabata's third basic relation, as described in [1]_.

    Parameters
    ----------
    d : ndarray
        Differences in keV between energies and threshold energy. Must be
        non-negative for real-valued results.
    c1 : float
        First coefficient of the basic relation.
    c2 : float
        Second coefficient of the basic relation.
    c3 : float
        Third coefficient of the basic relation.
    c4 : float
        Fourth coefficient of the basic relation.
    c5 : float
        Fifth coefficient of the basic relation.
    c6 : float
        Sixth coefficient of the basic relation.

    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``d``, in
        units of cm².

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    return _basic_i(d, c1, c2) / (1.0 + (d / c3) ** (c2 + c4) + (d / c5) ** (c2 + c6))


def _basic_iv(
    d: _NDArray[_np.float64],
    c1: float,
    c2: float,
    c3: float,
    c4: float,
    c5: float,
    c6: float,
    c7: float,
    c8: float,
) -> _NDArray[_np.float64]:
    """
    Tabata's fourth basic relation, as described in [1]_.

    Parameters
    ----------
    d : ndarray
        Differences in keV between energies and threshold energy. Must be
        non-negative for real-valued results.
    c1 : float
        First coefficient of the basic relation.
    c2 : float
        Second coefficient of the basic relation.
    c3 : float
        Third coefficient of the basic relation.
    c4 : float
        Fourth coefficient of the basic relation.
    c5 : float
        Fifth coefficient of the basic relation.
    c6 : float
        Sixth coefficient of the basic relation.
    c7 : float
        Seventh coefficient of the basic relation.
    c8 : float
        Eighth coefficient of the basic relation.

    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``d``, in
        units of cm².

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    return (
        _basic_i(d, c1, c2)
        * (1.0 + (d / c3) ** (c4 - c2))
        / (1.0 + (d / c5) ** (c4 + c6) + (d / c7) ** (c4 + c8))
    )


# Tabata's analytic expressions
def tab2_1_1(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    First fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return _basic_ii(d, c[1], c[2], c[3], c[4]) * _CM2_TO_M2


def tab2_1_2(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Second fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4])
        + c[5] * _basic_ii(d / c[6], c[1], c[2], c[3], c[4])
    ) * _CM2_TO_M2


def tab2_1_3(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Third fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4]) + _basic_ii(d, c[5], c[6], c[7], c[8])
    ) * _CM2_TO_M2


def tab2_1_4(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Fourth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4])
        + _basic_ii(d, c[5], c[6], c[7], c[8])
        + c[9] * _basic_ii(d / c[10], c[5], c[6], c[7], c[8])
    ) * _CM2_TO_M2


def tab2_1_5(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Fifth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4])
        + _basic_ii(d, c[5], c[6], c[7], c[8])
        + _basic_ii(d, c[9], c[10], c[11], c[12])
    ) * _CM2_TO_M2


def tab2_1_6(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Sixth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return _basic_iii(d, c[1], c[2], c[3], c[4], c[5], c[6]) * _CM2_TO_M2


def tab2_1_7(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Seventh fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4])
        + _basic_iii(d, c[5], c[2], c[6], c[7], c[8], c[4])
    ) * _CM2_TO_M2


def tab2_1_8(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Eighth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4])
        + _basic_iii(d, c[5], c[2], c[6], c[7], c[8], c[9])
    ) * _CM2_TO_M2


def tab2_1_9(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Ninth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_ii(d, c[1], c[2], c[3], c[4])
        + _basic_iii(d, c[5], c[6], c[7], c[8], c[9], c[4])
    ) * _CM2_TO_M2


def tab2_1_10(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Tenth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_iii(d, c[1], c[2], c[3], c[4], c[5], c[6])
        + c[7] * _basic_iii(d / c[8], c[1], c[2], c[3], c[4], c[5], c[6])
    ) * _CM2_TO_M2


def tab2_1_11(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Eleventh fit function template described by Tabata in the first paper of
    [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_iii(d, c[1], c[2], c[3], c[4], c[5], c[6])
        + _basic_ii(d, c[7], c[8], c[9], c[10])
    ) * _CM2_TO_M2


def tab2_1_12(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Twelfth fit function template described by Tabata in the first paper of [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_iii(d, c[1], c[2], c[3], c[4], c[5], c[6])
        + _basic_ii(d, c[7], c[8], c[9], c[10])
        + c[11] * _basic_ii(d / c[12], c[7], c[8], c[9], c[10])
    ) * _CM2_TO_M2


def tab2_1_13(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Thirteenth fit function template described by Tabata in the first paper of
    [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return (
        _basic_iii(d, c[1], c[2], c[3], c[4], c[5], c[6])
        + _basic_iii(d, c[7], c[8], c[9], c[10], c[11], c[12])
    ) * _CM2_TO_M2


def tab2_1_14(
    energies: _ArrayLike,
    coefficients: _ArrayLike,
    **ctx,
) -> _NDArray[_np.float64]:
    """
    Fourteenth fit function template described by Tabata in the first paper of
    [1]_

    Parameters
    ----------
    energies : array_like
        Energies in eV at which to evaluate the cross-section.
    coefficients : array_like
        Tabata's coefficients, in order of increasing degree, as stored in
        CroXe. ``coefficients[0]`` is the threshold energy of the process.
    ctx : dict[str, float]
        Context-dependent keyword arguments, which provide additional parameters
        when they are needed for calculations.

        This function does not require any key in ``ctx``.


    Returns
    -------
    s : ndarray
        Array of evaluated cross-sections, with the same shape as ``energies``,
        in units of m².

    Notes
    -----
    The first coefficient (index 0) accepted by any of the analytic expressions
    is what Tabata defines as the threshold energy of the process. For this
    function to be real valued, due to how the four basic relations are defined,
    every item in ``energies`` must be greater than ``coefficients[0]``, which
    is true if every energy value in ``energies`` falls within the provided
    domain, since ``e_min > coefficients[0]`` for every set of fit parameters
    obtained from Tabata's work and stored in CroXe.

    Since every public function defined in :py:mod:`pycroxe.fitfunctions` must
    share the same signature, ``ctx`` is passed but ignored, as no extra
    parameter is required by this function for cross-section calculations.

    References
    ----------
    .. [1] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic
       and Molecular Collision Cross Sections (2)", *IDEA*, 2018
       (https://doi.org/10.13140/RG.2.2.26689.07521)
    """
    energies = _np.asarray(energies, dtype=_np.float64)
    c = _np.asarray(coefficients, dtype=_np.float64)
    d = (energies - c[0]) * _EV_TO_KEV
    return _basic_iv(d, c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8]) * _CM2_TO_M2
