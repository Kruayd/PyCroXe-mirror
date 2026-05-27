"""
======================
Fit function templates
======================

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

Usage
-----
:py:mod:`pycroxe.fitfunctions` provides a simple interface to interact with the
fit functions stored in it: by providing to
:py:func:`pycroxe.fitfunctions.get_fit_function` a string corresponding to any
of the values in the column ``function_name`` of table ``fit_templates`` in
CroXe, you will retrieve the implementation in this API of that very function.

If you wish to implement a new function without directly modifying
:py:mod:`pycroxe`, you can add it to :py:data:`pycroxe.fitfunctions.REGISTRY`::

    REGISTRY["NEWTAG"] = new_function

just remember that your ``new_function`` must follow the
:py:class:`pycroxe.fitfunctions.FitFunction` protocol, which you can directly
use in your code for type hinting.

Notes
-----
CroXe and this API store and accept energies in eV and cross-section in m². In
the case of authors using different units of measurments (usually cm² for
cross-sections, and eV/amu [1]_ or keV [2]_ for energies), the conversion is
handled internally by each fit function.

Tabata's functions in this module are registered with a leading triad of numbers
assigned in such a way that the first number indicates in which volume of the
"*Atomic and Molecular Collision Cross Sections*" the function appears, the
second number corresponds to the n-th paper within the volume, and the last one
is the label assigned by Tabata himself to the function, within the paper.
Following this convention, function ``tab2_1_4`` is, hence, function 4 in the
first paper of "*Atomic and Molecular Collision Cross Sections (2)*" [2]_.

Checking whether some energy value falls within the domain of some registered
function or not, is responsibility of the evaluation layer of each
:py:mod:`pycroxe` sub-module

Currently implemented functions:

* ``REGISTRY["CHEB"]``: a Chebyshev polynomial-based fit described by C. F.
  Barnett in [1]_
* ``REGISTRY["TAB2_1_*"]``: the 14 analytic expressions described by T. Tabata in
  the first paper of [2]_

References
----------
.. [1] C. F. Barnett, "Atomic Data for Fusion Volume 1: Collisions of H, H2, He
   and Li Atoms and Ions with Atoms and Molecules", *Controlled Fusion Atomic
   Data Center*, 1990 (https://doi.org/10.2172/6570226)

.. [2] T. Tabata, "The Collected Works of Tatsuo Tabata Volume 17: Atomic and
   Molecular Collision Cross Sections (2)", *IDEA*, 2018
   (https://doi.org/10.13140/RG.2.2.26689.07521)
"""

from ._registry import FitFunction, REGISTRY, get_fit_function

__all__: list[str] = ["FitFunction", "REGISTRY", "get_fit_function"]
