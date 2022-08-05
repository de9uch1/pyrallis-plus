Pyrallis+
#########

This is an enhanced `pyrallis <https://github.com/eladrich/pyrallis>`_, dataclass-based simple configuration library.

`Pyrallis <https://github.com/eladrich/pyrallis>`_ is an awesome configuration library based on the python dataclass.
It is designed to be a simple and clean library.
This library adds some features to Pyrallis at the expense of simplicity.

Features
========
These extended features are available by just importing :code:`pyrallis_plus`:

Boolean option
--------------
:code:`store_true` and :code:`store_false` are automatically set from the default value.

.. code-block:: python

   from dataclasses import dataclass
   import pyrallis
   import pyrallis_plus

   @dataclass
   class Config:
       bool_option: bool = False  # Set `store_true` as action.

   @pyrallis.wrap()
   def main(cfg: Config):
       print(pyrallis.dump(cfg))

List option
-----------
:code:`nargs="*"` will be automatically set in list fields.

.. code-block:: python

   from dataclasses import dataclass, field
   import pyrallis
   import pyrallis_plus

   @dataclass
   class Config:
       names: List[str] = field(default_factory=[])  # Set `nargs="*"`.

   @pyrallis.wrap()
   def main(cfg: Config):
       print(pyrallis.dump(cfg))


Help option
-----------
:code:`-h` option can be also used as the short option of :code:`--help`

Alias
-----
- Defined by :code:`metadata` in dataclass fields.
- :code:`pyrallis.field()` can also define aliases by the :code:`alias` argument.

Installation
============

::

   % pip install git+https://github.com/de9uch1/pyrallis-plus.git

Usage
=====

Just import :code:`pyrallis_plus` and you can use the :code:`pyrallis` module with the extension.
