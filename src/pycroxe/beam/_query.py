"""
==================================
Beam-on-target data querying layer
==================================

Private module for beam-on-target processes related queries.

Data classes
------------

.. autosummary::
    :toctree: generated/

    BeamProcessRecord
    BeamFitRecord

Functions
---------

.. autosummary::
    :toctree: generated/

    get_processes
    get_descendant_processes_by_projectiles
    get_fits_by_process

Types
-----

.. autosummary::
    :toctree: generated/

    SortKey

"""

from collections.abc import Sequence as _Sequence
from dataclasses import dataclass as _dataclass
from typing import Literal as _Literal

import numpy as _np
from numpy.typing import NDArray as _NDArray
from sqlalchemy import Row as _Row
from sqlalchemy import ColumnElement as _ColumnElement
from sqlalchemy import select as _select
from sqlalchemy import func as _func

from .._connection import CroXeConnection as _CroXeConnection

__all__: list[str] = [
    "SortKey",
    "BeamProcessRecord",
    "BeamFitRecord",
    "get_processes",
    "get_descendant_processes_by_projectiles",
    "get_fits_by_process",
]

# Type for the criterion by which beam-on-target queries can sort their results.
type SortKey = _Literal["rms", "year"]


@_dataclass(frozen=True, slots=True)
class BeamProcessRecord:
    """
    All data needed to indentify beam-on-target processes.

    Attributes
    ----------
    projectile : str
        Chemical symbol of the projectile species.
    target : str
        Chemical symbol of the target species.
    product : str
        Chemical symbol of the product species.
    product_frame : str
        Reference frame of the product after the collision
        (``'projectile'`` or ``'target'``).
    """

    projectile: str
    target: str
    product: str
    product_frame: str


@_dataclass(frozen=True, slots=True)
class BeamFitRecord:
    """
    All data needed to evaluate fits of beam-on-target processes.

    Attributes
    ----------
    projectile : str
        Chemical symbol of the projectile species.
    target : str
        Chemical symbol of the target species.
    product : str
        Chemical symbol of the product species.
    product_frame : str
        Reference frame of the product after the collision
        (``'projectile'`` or ``'target'``).
    source_tag : str
        Bibliographic source identifier (e.g. ``'Barnett1990'``).
    fit_index : int
        Ordering index for multiple fits from the same source on the same
        process (1-based).
    function_name : str
        Key into the fit function registry (e.g. ``'CHEB'``, ``'TAB2_1_3'``).
    e_min : float
        Lower bound of fit validity in eV.
    e_max : float
        Upper bound of fit validity in eV.
    rms : float or None
        Relative RMS deviation of the fit.
    coefficients : ndarray
        Ordered array of fit coefficients.
    projectile_mass : float
        Atomic/molecular mass of the projectile in amu.
    """

    projectile: str
    target: str
    product: str
    product_frame: str
    source_tag: str
    fit_index: int
    function_name: str
    e_min: float
    e_max: float
    rms: float | None
    coefficients: _NDArray[_np.float64]
    projectile_mass: float

    # numpy arrays are not hashable; identity is defined on scalar fields only
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BeamFitRecord):
            return NotImplemented
        return (
            self.projectile == other.projectile
            and self.target == other.target
            and self.product == other.product
            and self.product_frame == other.product_frame
            and self.source_tag == other.source_tag
            and self.fit_index == other.fit_index
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.projectile,
                self.target,
                self.product,
                self.product_frame,
                self.source_tag,
                self.fit_index,
            )
        )


def get_processes(
    conn: _CroXeConnection,
    projectiles: list[str] | None = None,
    targets: list[str] | None = None,
    products: list[str] | None = None,
    product_frame: str = "projectile",
) -> list[BeamProcessRecord]:
    """
    List all beam-on-target processes stored in the database. Optionally filters
    by projectiles, targets or products.

    Parameters
    ----------
    conn : :py:class:`pycroxe.CroXeConnection`
        An open :py:class:`pycroxe.CroXeConnection`.
    projectiles : list[str], optional
        If given, restrict results to processes involving these projectile
        species.
    targets : list[str], optional
        If given, restrict results to processes involving these target species.
    products : list[str], optional
        If given, restrict results to processes involving these products
        species.
    product_frame : str, optional
        Reference frame of the product after the collision (default:
        ``'projectile'``).

    Returns
    -------
    processes : list[:py:class:`pycroxe.beam.BeamProcessRecord`]
        List of processes in the form of
        :py:class:`pycroxe.beam.BeamProcessRecord`, ordered by target first,
        then projectile, then product.
    """
    beam_processes_table = conn.get_table_by_name("beam_processes")
    sql = _select(
        beam_processes_table.c.projectile,
        beam_processes_table.c.target,
        beam_processes_table.c.product,
        beam_processes_table.c.product_frame,
    )
    if projectiles is not None:
        sql = sql.where(beam_processes_table.c.projectile.in_(projectiles))
    if targets is not None:
        sql = sql.where(beam_processes_table.c.target.in_(targets))
    if products is not None:
        sql = sql.where(beam_processes_table.c.product.in_(products))
    sql = sql.where(beam_processes_table.c.product_frame == product_frame)

    sql = sql.order_by(
        beam_processes_table.c.target,
        beam_processes_table.c.projectile,
        beam_processes_table.c.product,
    )

    return [_row_to_beam_process_record(row) for row in conn.raw.execute(sql)]


def get_descendant_processes_by_projectiles(
    conn: _CroXeConnection,
    initial_projectiles: list[str],
    target: str,
    product_frame: str = "projectile",
) -> list[BeamProcessRecord]:
    """
    Return all beam-on-target processes reachable from projectile in
    ``initial_projectiles`` .

    This function leverages a recursive CTE to traverse a beam-on-target
    processes graph built from the ``beam_processes`` table.

    Parameters
    ----------
    conn : :py:class:`pycroxe.CroXeConnection`
        An open :py:class:`pycroxe.CroXeConnection`.
    inital_projectiles : list[str]
        List of chemical symbols of the starting projectile species.
    target : str
        Chemical symbol of the target species.
    product_frame : str, optional
        Reference frame of the product after the collision (default:
        ``'projectile'``).

    Returns
    -------
    processes : list[:py:class:`pycroxe.beam.BeamProcessRecord`]
        All processes reachable from starting projectile species.

    Raises
    ------
    ValueError
        If ``inital_projectiles`` is empty.
    """
    if not initial_projectiles:
        raise ValueError("initial_projectiles must contain at least one symbol.")

    beam_processes_table = conn.get_table_by_name("beam_processes")

    cte_anchor = (
        _select(
            beam_processes_table.c.projectile,
            beam_processes_table.c.target,
            beam_processes_table.c.product,
            beam_processes_table.c.product_frame,
        )
        .where(
            beam_processes_table.c.projectile.in_(initial_projectiles)
            & (beam_processes_table.c.target == target)
            & (beam_processes_table.c.product_frame == product_frame)
        )
        .cte(recursive=True)
    )

    cte_full = cte_anchor.union(
        _select(
            beam_processes_table.c.projectile,
            beam_processes_table.c.target,
            beam_processes_table.c.product,
            beam_processes_table.c.product_frame,
        ).where(
            (beam_processes_table.c.projectile == cte_anchor.c.product)
            & (beam_processes_table.c.target == target)
            & (beam_processes_table.c.product_frame == product_frame)
        )
    )

    sql = _select(
        cte_full.c.projectile,
        cte_full.c.target,
        cte_full.c.product,
        cte_full.c.product_frame,
    )

    return [_row_to_beam_process_record(row) for row in conn.raw.execute(sql)]


def get_fits_by_process(
    conn: _CroXeConnection,
    projectile: str,
    target: str,
    product: str,
    product_frame: str = "projectile",
    sort_by: _Sequence[SortKey] = ("year", "rms"),
) -> list[BeamFitRecord]:
    """
    Return all the possible fits for the given process, identified by
    ``projectile``, ``target``, ``product``, ``product_frame``, and
    sorted according to ``sort_by``.

    Parameters
    ----------
    conn : :py:class:`pycroxe.CroXeConnection`
        An open :py:class:`pycroxe.CroXeConnection`.
    projectile : str
        Chemical symbol of the projectile species.
    target : str
        Chemical symbol of the target species.
    product : str
        Chemical symbol of the product species.
    product_frame : str, optional
        Reference frame of the product after the collision (default:
        ``'projectile'``).
    sort_by : Sequence[:py:data:`pycroxe.beam.SortKey`]
        Ordered sequence of :py:data:`pycroxe.beam.SortKey` values that
        determines the ``ORDER BY`` clause.  The first key is the primary sort
        criterion, the second (if present) is the tiebreaker, and so on.

    Returns
    -------
    fits : list[:py:class:`pycroxe.beam.BeamFitRecord`]
        List of all the possible fits for the process, in the requested order.
        The list can be empty.

    Raises
    ------
    ValueError
        If ``sort_by`` is empty.
    """
    if not sort_by:
        raise ValueError("sort_by must contain at least one SortKey.")

    species_table = conn.get_table_by_name("species")
    sources_table = conn.get_table_by_name("sources")
    beam_fit_params_table = conn.get_table_by_name("beam_fit_params")
    beam_fit_coefficients_table = conn.get_table_by_name("beam_fit_coefficients")

    sort_column_map: dict[str, list[_ColumnElement]] = {
        # MariaDB doesn't support NULLS LAST statements
        # According to
        # https://mariadb.com/docs/server/reference/data-types/null-values#ordering
        # ny NULL values are considered to have the lowest value. So ordering
        # in ASC (default sort order) need some trick (e.g. sorting first by a
        # column that sorts NULL last)
        # ISNULL is MariaDB-specific!!!
        "rms": [
            _func.isnull(beam_fit_params_table.c.rms),
            beam_fit_params_table.c.rms.asc(),
        ],
        # According to
        # https://mariadb.com/docs/server/reference/data-types/null-values#ordering
        # ny NULL values are considered to have the lowest value. So ordering
        # in DESC order will see the NULL values appearing last
        "year": [
            sources_table.c.year.desc(),
        ],
    }
    order_by_clauses = [clause for k in sort_by for clause in sort_column_map[k]]

    sql = (
        _select(
            beam_fit_params_table.c.projectile,
            beam_fit_params_table.c.target,
            beam_fit_params_table.c.product,
            beam_fit_params_table.c.product_frame,
            beam_fit_params_table.c.source_tag,
            beam_fit_params_table.c.fit_index,
            beam_fit_params_table.c.function_name,
            beam_fit_params_table.c.e_min,
            beam_fit_params_table.c.e_max,
            beam_fit_params_table.c.rms,
            species_table.c.mass,
            sources_table.c.year,
            _func.aggregate_strings(beam_fit_coefficients_table.c.coeff_order, ","),
            _func.aggregate_strings(beam_fit_coefficients_table.c.coeff_value, ","),
        )
        .join_from(
            beam_fit_params_table,
            species_table,
            species_table.c.symbol == beam_fit_params_table.c.projectile,
        )
        .join_from(
            beam_fit_params_table,
            sources_table,
            sources_table.c.source_tag == beam_fit_params_table.c.source_tag,
        )
        .join_from(
            beam_fit_params_table,
            beam_fit_coefficients_table,
            (
                beam_fit_coefficients_table.c.projectile
                == beam_fit_params_table.c.projectile
            )
            & (beam_fit_coefficients_table.c.target == beam_fit_params_table.c.target)
            & (beam_fit_coefficients_table.c.product == beam_fit_params_table.c.product)
            & (
                beam_fit_coefficients_table.c.product_frame
                == beam_fit_params_table.c.product_frame
            )
            & (
                beam_fit_coefficients_table.c.source_tag
                == beam_fit_params_table.c.source_tag
            )
            & (
                beam_fit_coefficients_table.c.fit_index
                == beam_fit_params_table.c.fit_index
            ),
        )
        .where(
            (beam_fit_params_table.c.projectile == projectile)
            & (beam_fit_params_table.c.target == target)
            & (beam_fit_params_table.c.product == product)
            & (beam_fit_params_table.c.product_frame == product_frame)
        )
        .group_by(
            beam_fit_params_table.c.projectile,
            beam_fit_params_table.c.target,
            beam_fit_params_table.c.product,
            beam_fit_params_table.c.product_frame,
            beam_fit_params_table.c.source_tag,
            beam_fit_params_table.c.fit_index,
        )
        .order_by(*order_by_clauses)
    )

    return [_row_to_beam_fit_record(row) for row in conn.raw.execute(sql)]


# Private helpers
def _row_to_beam_process_record(row: _Row) -> BeamProcessRecord:
    """
    Convert a raw SQLAlchemy row from :py:func:`pycroxe.beam.get_processes` to
    a :py:class:`pycroxe.beam.BeamProcessRecord`

    Parameters
    ----------
    row : :py:class:`sqlalchemy.engine.Row`
        Row from SQLAlchemy query.

    Returns
    -------
    process : :py:class:`pycroxe.beam.BeamProcessRecord`

    Notes
    -----
    Column order:

    0. ``projectile``
    1. ``target``
    2. ``product``
    3. ``product_frame``
    """
    return BeamProcessRecord(
        projectile=row[0],
        target=row[1],
        product=row[2],
        product_frame=row[3],
    )


def _row_to_beam_fit_record(row: _Row) -> BeamFitRecord:
    """
    Convert a raw SQLAlchemy row from
    :py:func:`pycroxe.beam.get_fits_by_process` to a
    :py:class:`pycroxe.beam.BeamFitRecord`.

    Parameters
    ----------
    row : :py:class:`sqlalchemy.engine.Row`
        Row from SQLAlchemy query.

    Returns
    -------
    fit : :py:class:`pycroxe.beam.BeamFitRecord`

    Notes
    -----
    Column order:

    0. ``projectile``
    1. ``target``
    2. ``product``
    3. ``product_frame``
    4. ``source_tag``
    5. ``fit_index``
    6. ``function_name``
    7. ``e_min``
    8. ``e_max``
    9. ``rms``
    10. ``projectile_mass``
    11. ``year``
    12. ``coeff_order``
    13. ``coeff_value``
    """
    coefficients_indexes = _np.fromstring(row[12], dtype=_np.intp, sep=",")
    coefficients_values = _np.fromstring(row[13], dtype=_np.float64, sep=",")
    coefficients = _np.empty_like(coefficients_values)
    coefficients[coefficients_indexes] = coefficients_values
    coefficients.setflags(write=False)

    return BeamFitRecord(
        projectile=row[0],
        target=row[1],
        product=row[2],
        product_frame=row[3],
        source_tag=row[4],
        fit_index=int(row[5]),
        function_name=row[6],
        e_min=float(row[7]),
        e_max=float(row[8]),
        rms=float(row[9]) if row[9] is not None else None,
        projectile_mass=float(row[10]),
        # row[11] is year, not stored in the record
        coefficients=coefficients,
    )
