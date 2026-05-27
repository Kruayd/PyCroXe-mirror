# Welcome to PyCroXe

The Python API that let you import data from
[CroXe](https://codeberg.org/Kruayd/CroXe), with intuitive calls and minimal
effort.

If you are looking for the database itself, visit:
[https://codeberg.org/Kruayd/CroXe](https://codeberg.org/Kruayd/CroXe).

## Table of contents

<!-- toc -->

- [Installation](#installation)
- [Example usage](#example-usage)
  - [tl;dr](#tldr)
  - [Connecting](#connecting)
  - [Retrieving species properties](#retrieving-species-properties)
  - [Retrieving beam-on-target processes cross-sections](#retrieving-beam-on-target-processes-cross-sections)
- [Full documentation](#full-documentation)
- [Contributing](#contributing)
- [License](#license)

<!-- tocstop -->

## Installation

At this development stage PyCroXe is not yet public on
[PyPI](https://pypi.org/), hence just running `pip install pycroxe` won't work.
You can, though, clone this repo to your machine and install PyCroXe from it:

```bash
git clone https://codeberg.org/Kruayd/PyCroXe.git
pip install ./PyCroXe
```

> [!IMPORTANT]
> PyCroXe requires Python 3.12 or newer!

## Example usage

### tl;dr

```python
import numpy as np
from pycroxe import connect, get_species_properties
from pycroxe.beam import get_cross_sections_by_projectiles

energies = np.geomspace(10, 1e5, 200) # energies in eV

with connect() as conn:
    sigma = get_cross_sections_by_projectiles(
        conn,
        energies,
        initial_projectiles=["H3+", "H2+", "H+"],
        target="H2",
    )

    species_data = get_species_properties(
        conn,
        symbols=sigma.coords["product"].to_numpy().tolist(),
    )
```

But please, find some time to read the rest of this README or the official docs!

### Connecting

PyCroXe provides a `connect` function that can be used, as the name obviously
suggests, to connect to any network-reachable instance of CroXe.

The intended usage is within a `with` statement; this will make `connect`, if
no argument is provided, return an instance of a `CroXeConnection` class,
acting as a context manager, with an open connection pointing towards the
default URL `mariadb+mariadbconnector://croxe-guest@localhost/CroXe`:

```python
from pycroxe import connect

with connect() as conn:
    ...
```

PyCroXe URLs follow the
[SQLAlchemy pattern](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)
(`dialect+driver://username@host:port/database`) and can be provided to the
`connect` function, in order of descending precedence, by:

1. directly passing them as argument

   ```python
   with connect(
       "mariadb+mariadbconnector://user@server.institute.org/CroXe"
   ) as conn:
       ...
   ```

2. setting up the environment variable `CROXE_DB`

   ```bash
   # if using bash
   export CROXE_DB="mysql+pymysql://user@server.institute.org/CroXe"
   ```

3. changing specific parts of the default URL with keyword arguments

   ```python
   with connect(
        host="server.institute.org",
        user="user",
        connector="mariadb+mariadbconnector",
        database="CroXe_2_electric_boogaloo"
   ) as conn:
        ...
   ```

> [!NOTE]
> `connect` can also be used outside `with` statements, but notice that this
> will return a closed instance of a `CroXeConnection` class that must be
> opened and closed manually with the corresponding methods:
>
> ```python
> from pycroxe import connect
>
> conn = connect()
> conn.open()
> ...
> conn.close()
> ```
>
> At this point, if you really wish not to use a `with` statement, you can just
> use the `CroXeConnection` class instance builder, to which you can provide
> URLs in the same manner as to `connect`:
>
> ```python
> from pycroxe import CroXeConnection
>
> conn = CroXeConnection("mysql+pymysql://user@server.institute.org/CroXe")
> conn.open()
> ...
> conn.close()
> ```

> [!CAUTION]
> Using `connect` and/or `CroXeConnection` outside `with` statements is
> strongly discouraged!

### Retrieving species properties

Function `get_species_properties` will return a [xarray Dataset](https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataset)
of properties of all the species stored in CroXe. If given the `symbols`
keyword argument, data will be limited only to the chosen species:

```python
from pycroxe import connect, get_species_properties

with connect() as conn:
    species_data = get_species_properties(
        conn,
        symbols=["H+", "H2"],
    )
```

### Retrieving beam-on-target processes cross-sections

PyCroXe provides the `beam` module, which in turn provides the
`get_cross_sections_by_projectiles` function.
`get_cross_sections_by_projectiles` will first recursively find all processes
that may derive from the given list of initial projectile species, and then
return a 3D tensor of evaluated cross-sections, in the form of a
[xarray DataArray](https://docs.xarray.dev/en/stable/user-guide/data-structures.html#dataarray),
with first dimension indexing energy values, the second indexing product
species, and the last one indexing projectiles:

```python
import numpy as np
from pycroxe import connect
from pycroxe.beam import get_cross_sections_by_projectiles

energies = np.geomspace(10, 1e5, 200) # energies in eV

with connect() as conn:
    sigma = get_cross_sections_by_projectiles(
        conn,
        energies,
        initial_projectiles=["H3+", "H2+", "H+"],
        target="H2",
    )
```

## Full documentation

Coming soon!

## Contributing

Right now you can suggest changes through
[e-mail](mailto:luca.cinnirella@protonmail.com), but soon some more standard
ways of contributing will be available.

## License

PyCroXe is free as in freedom and licensed under the [GPL v3](./LICENSE).
