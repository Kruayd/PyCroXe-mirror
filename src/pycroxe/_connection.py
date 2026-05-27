"""
==================
Connection manager
==================

Private module providing tools for managing connection to CroXe

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

Notes
-----
If no ``url`` is passed to :py:func:`pycroxe.connect`, or directly to
:py:class:`pycroxe.CroXeConnection`, they will first check if the ``CROXE_DB``
environment variable is set; if it is not, they will build a URL with the given
``connector``, ``user``, ``host`` and ``database`` parameters, which with
default values evaluates to::

    mariadb+mariadbconnector://croxe-guest@localhost/CroXe

Since :py:mod:`pycroxe` leverages
`SQLAlchemy <https://www.sqlalchemy.org/>`, connection URLs must follow
SQLAlchemy pattern::

    dialect+driver://username:password@host:port/database
"""

import os as _os
from types import TracebackType as _TracebackType
from typing import Self as _Self

from sqlalchemy import Connection as _Connection
from sqlalchemy import Engine as _Engine
from sqlalchemy import MetaData as _MetaData
from sqlalchemy import Table as _Table
from sqlalchemy import create_engine as _create_engine
from sqlalchemy import select as _select

__all__: list[str] = ["CroXeConnection", "connect"]


class CroXeConnection:
    """
    Thin wrapper around a SQLAlchemy :py:class:`sqlalchemy.engine.Connection`.

    Manages engine creation, connection lifecycle, and exposes the raw
    SQLAlchemy :py:class:`sqlalchemy.engine.Connection` for use by the query
    layer.

    Parameters
    ----------
    url : str, optional
        SQLAlchemy connection URL.  If ``None``, the value of the
        ``CROXE_DB`` environment variable is used; if that is also unset, a URL
        will be constructed using the ``connector``, ``user``, ``host`` and
        ``database`` parameters.
        With default values, the constructed URL is::

            mariadb+mariadbconnector://croxe-guest@localhost/CroXe

    host : str, optional
        Name or IP address of the machine hosting the database (default:
        ``localhost``). Ports can be selected by appending a colon, followed by
        the port number, to the host name or IP address::

            hostname:portnumber

    user : str, optional
        Name of the loggin user (default: ``croxe-guest``). Note that passwords
        can be used as well, by appending them with a leading colon to the
        username, though it is **strongly discouraged** since this method
        exposes the password::

            username:password

    connector : str, optional
        Combination of SQLAlchemy dialect and driver (default:
        ``mariadb+mariadbconnector``).
    database : str, optional
        Database to be used (default: ``CroXe``).

    engine_kwargs : dict, optional
        Extra keyword arguments forwarded verbatim to
        :py:func:`sqlalchemy.engine.create_engine`
        (e.g. ``pool_pre_ping=True``).

    Attributes
    ----------
    raw : :py:class:`sqlalchemy.engine.Connection`
        The underlying :py:class:`sqlalchemy.engine.Connection` object.
    """

    def __init__(
        self,
        url: str | None = None,
        host: str = "localhost",
        user: str = "croxe-guest",
        connector: str = "mariadb+mariadbconnector",
        database: str = "CroXe",
        **engine_kwargs,
    ) -> None:
        resolved_url = url or _os.environ.get(
            "CROXE_DB", f"{connector}://{user}@{host}/{database}"
        )
        self._engine: _Engine = _create_engine(resolved_url, **engine_kwargs)
        self._conn: _Connection | None = None
        self._metadata: _MetaData = _MetaData()

    # Low level opening an closing
    def open(self) -> None:
        """
        Open connection to the database.

        Notes
        -----
        If not using as a context manager, this method must be called before
        accessing the :py:attr:`pycroxe.CroXeConnection.raw` connection.
        """
        if self._conn is not None:
            raise RuntimeError("Connection is already open.")
        self._conn = self._engine.connect()

    def close(self) -> None:
        """
        Close connection to the database

        Notes
        -----
        If not using as a context manager, this method must be called explicitly
        """
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # Context manager opening and closing
    def __enter__(self) -> _Self:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: _TracebackType | None,
    ) -> None:
        self.close()

    @property
    def raw(self) -> _Connection:
        """
        The underlying :py:class:`sqlalchemy.engine.Connection`.

        Raises
        ------
        RuntimeError
            If accessed before :py:meth:`pycroxe.CroXeConnection.open`
            has been called.
        """
        if self._conn is None:
            raise RuntimeError(
                "Database connection is not open.\n"
                "Use CroXeConnection as a context manager or call .open() first."
            )
        return self._conn

    def get_table_by_name(self, tablename: str) -> _Table:
        """
        *Reflect* requested table into a :py:class`sqlalchemy.schema.Table`
        object and return it. Tables that have been already *reflected* once
        won't be *reflected* again: the method will just return the existing
        :py:class`sqlalchemy.schema.Table` object.

        Parameters
        ----------
        tablename : str
            Name of any table in CroXe.

        Returns
        -------
        table : :py:class`sqlalchemy.schema.Table`
            SQLAlchemy :py:class`sqlalchemy.schema.Table` object reflecting the
            corresponding CroXe table.
        """
        return _Table(tablename, self._metadata, autoload_with=self._engine)

    # Convenience method
    def ping(self) -> bool:
        """
        Convenience method used to test database connection.
        It executes ``SELECT 1`` under the hood.

        Returns
        -------
        b : bool
            Returns ``True`` if test was successful.
        """
        try:
            self.raw.execute(_select(1))
            return True
        except Exception:
            return False


def connect(
    url: str | None = None,
    host: str = "localhost",
    user: str = "croxe-guest",
    connector: str = "mariadb+mariadbconnector",
    database: str = "CroXe",
    **engine_kwargs,
) -> CroXeConnection:
    """
    If used outside of a ``with`` statement, create and return an *unopened*
    :py:class:`pycroxe.CroXeConnection`.
    The intended use is within a ``with`` statement, which returns instead an
    **open** :py:class:`pycroxe.CroXeConnection`::

        with connect() as conn:
            ...

    Parameters
    ----------
    url : str, optional
        SQLAlchemy connection URL.  If ``None``, the value of the
        ``CROXE_DB`` environment variable is used; if that is also unset, a URL
        will be constructed using the ``connector``, ``user``, ``host`` and
        ``database`` parameters.
        With default values, the constructed URL is::

            mariadb+mariadbconnector://croxe-guest@localhost/CroXe

    host : str, optional
        Name or IP address of the machine hosting the database (default:
        ``localhost``). Ports can be selected by appending a colon, followed by
        the port number, to the host name or IP address::

            hostname:portnumber

    user : str, optional
        Name of the loggin user (default: ``croxe-guest``). Note that passwords
        can be used as well, by appending them with a leading colon to the
        username, though it is **strongly discouraged** since this method exposes
        the password::

            username:password

    connector : str, optional
        Combination of SQLAlchemy dialect and driver (default:
        ``mariadb+mariadbconnector``).
    database : str, optional
        Database to be used (default: ``CroXe``).

    engine_kwargs : dict, optional
        Extra keyword arguments forwarded verbatim to
        :py:func:`sqlalchemy.engine.create_engine`
        (e.g. ``pool_pre_ping=True``).

    Returns
    -------
    conn : :py:class:`pycroxe.CroXeConnection`
        An instance ready to be used, possibly as a context manager.
    """
    return CroXeConnection(url, host, user, connector, database, **engine_kwargs)
