"""
======================================
Generic high-level provisionment layer
======================================

Private module for provisionment of generic structured data, such as species
properties.

Functions
---------

.. autosummary
    :toctree: generated/

    get_species_properties

"""

from sqlalchemy import select as _select

import numpy as _np
import xarray as _xr
from xarray import DataArray as _DataArray
from xarray import Dataset as _Dataset

from ._connection import CroXeConnection as _CroXeConnection


def get_species_properties(
    conn: _CroXeConnection,
    symbols: list[str] | None = None,
) -> _Dataset:
    """
    Return properties of selected species by ``symbols`` in the form of a
    :py:class:`xarray:Dataset`.

    Parameters
    ----------
    conn : :py:class:`pycroxe.CroXeConnection`
        An open :py:class:`pycroxe.CroXeConnection`.
    symbols : list[str], optional
        If given, get properties only for chosen species.

    Returns
    -------
    species_properties_dataset: :py:class:`xarray.Dataset`
        Dataset providing masses and charges of the retrieved species, ordered
        by species chemical symbols.
    """
    species_table = conn.get_table_by_name("species")
    sql = _select(
        species_table.c.symbol,
        species_table.c.mass,
        species_table.c.charge,
    )
    if symbols is not None:
        sql = sql.where(species_table.c.symbol.in_(symbols))
    sql = sql.order_by(species_table.c.symbol)

    symbol_column: list[str] = []
    mass_column: list[float] = []
    charge_column: list[int] = []

    for row in conn.raw.execute(sql):
        symbol_column.append(row[0])
        mass_column.append(float(row[1]))
        charge_column.append(int(row[2]))

    mass_array: _DataArray = _xr.DataArray(
        _np.array(mass_column, dtype=_np.float64),
        dims="species",
        coords=[symbol_column],
        name="Atomic/molecular mass of species",
        attrs={"units": "amu"},
    )

    charge_array: _DataArray = _xr.DataArray(
        _np.array(charge_column, dtype=_np.int_),
        dims="species",
        coords=[symbol_column],
        name="Electric charge of species",
        attrs={"units": "elementary charge"},
    )

    species_dataset: _Dataset = _xr.Dataset(
        data_vars={
            "mass": mass_array,
            "charge": charge_array,
        },
        # coords is inferred by provided DataArray
        attrs={
            "name": "Species properties",
            "mass units": "amu",
            "charge units": "elementary charge",
        },
    )

    return species_dataset
