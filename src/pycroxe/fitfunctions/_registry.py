"""
==========================================
Fit functions registry and retrieval logic
==========================================

Private module for fit functions retrieval logic

Protocol classes
----------------

.. autosummary::
    :toctree: generated/

    FitFunction

Constants
---------

.. autosummary::
    :toctree: generated/

    REGISTRY

Functions
---------

.. autosummary::
    :toctree: generated/

    get_fit_function

Notes
-----
Every fit function stored in CroXe ``fit_templates`` table has a corresponding
Python callable registered in this module under its ``function_name`` key.
All registered functions share the same signature::

    fn(
        energies    : ArrayLike,          # projectile energy in eV
        coefficients: ArrayLike,          # fit coefficients from DB
        **ctx,                            # template-specific context
    ) -> NDArray[np.float64]              # cross-section in m²

This allows for the evaluation layers of the various :py:mod:`pycroxe`
sub-modules (such as :py:mod:`pycorxe.beam`) to dispatch calls without needing
to know which template is being used.
"""

from typing import Protocol as _Protocol

import numpy as np
from numpy.typing import ArrayLike as _ArrayLike
from numpy.typing import NDArray as _NDArray

from ._barnett import cheb
from ._tabata import (
    tab2_1_1,
    tab2_1_2,
    tab2_1_3,
    tab2_1_4,
    tab2_1_5,
    tab2_1_6,
    tab2_1_7,
    tab2_1_8,
    tab2_1_9,
    tab2_1_10,
    tab2_1_11,
    tab2_1_12,
    tab2_1_13,
    tab2_1_14,
)

__all__: list[str] = ["FitFunction", "REGISTRY", "get_fit_function"]


class FitFunction(_Protocol):
    """
    Protocol class describing the uniform signature for every registered
    fit function.

    Using a ``Protocol`` rather than a bare ``Callable`` alias allows static
    type checkers to verify the full signature, including the variadic
    ``**ctx``, while keeping :py:data:`pycroxe.fitfunctions.REGISTRY` open to
    any compliant callable.
    """

    def __call__(
        self,
        energies: _ArrayLike,
        coefficients: _ArrayLike,
        **ctx: float,
    ) -> _NDArray[np.float64]:
        """
        Uniform call signature for every registered fit function.

        Parameters
        ----------
        energies : array_like
            Energies in eV at which to evaluate the cross-section.
        coefficients : array_like
            Function coefficients, in order of increasing degree, as stored in
            CroXe.
        ctx : dict[str, float]
            Context-dependent keyword arguments, which provide additional parameters
            when they are needed for calculations.

        Returns
        -------
        s : ndarray
            Array of evaluated cross-sections, with the same shape as
            ``energies``, in units of m².
        """
        ...


REGISTRY: dict[str, FitFunction] = {
    "CHEB": cheb,
    "TAB2_1_1": tab2_1_1,
    "TAB2_1_2": tab2_1_2,
    "TAB2_1_3": tab2_1_3,
    "TAB2_1_4": tab2_1_4,
    "TAB2_1_5": tab2_1_5,
    "TAB2_1_6": tab2_1_6,
    "TAB2_1_7": tab2_1_7,
    "TAB2_1_8": tab2_1_8,
    "TAB2_1_9": tab2_1_9,
    "TAB2_1_10": tab2_1_10,
    "TAB2_1_11": tab2_1_11,
    "TAB2_1_12": tab2_1_12,
    "TAB2_1_13": tab2_1_13,
    "TAB2_1_14": tab2_1_14,
}


def get_fit_function(function_name: str) -> FitFunction:
    """
    For a given template name from ``CroXe.fit_templates.function_name``,
    return its API implementation.

    Parameters
    ----------
    function_name : str
        The ``function_name`` key as stored in ``CroXe.fit_templates``.

    Returns
    -------
    f : FitFunction
        The corresponding API implementation.

    Raises
    ------
    KeyError
        If ``function_name`` is not present in
        :py:data:`pycroxe.fitfunctions.REGISTRY`. This most likely means a new
        template was added to the database without a matching API
        implementation.
    """
    try:
        return REGISTRY[function_name]
    except KeyError:
        registered = ", ".join(sorted(REGISTRY))
        raise KeyError(
            f"No fit function registered for '{function_name}'. "
            f"Registered templates: {registered}"
        ) from None
