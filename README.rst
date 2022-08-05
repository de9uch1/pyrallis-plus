Pyrallis+
#########

This is an enhanced `pyrallis <https://github.com/eladrich/pyrallis>`_, dataclass-based simple configuration library.

`Pyrallis <https://github.com/eladrich/pyrallis>`_ is an awesome configuration library based on the python dataclass.
It is designed to be a simple and clean library.
This library adds some features to Pyrallis at the expense of simplicity.

Features
========
These extended features are available:

Boolean option
--------------
:code:`store_true` and :code:`store_false` are automatically set from the default value.

.. code-block:: python

   from dataclasses import dataclass
   import pyrallis_plus

   @dataclass
   class Config:
       bool_option: bool = False  # Set `store_true` as action.

   @pyrallis_plus.wrap()
   def main(cfg: Config):
       print(pyrallis_plus.dump(cfg))


Help option
-----------
:code:`-h` option can be also used as the short option of :code:`--help`

Alias
-----
- Defined by :code:`metadata` in dataclass fields.
- :code:`pyrallis_plus.field()` can also define aliases by the :code:`alias` argument.

Installation
============

::

   % pip install git+https://github.com/de9uch1/pyrallis-plus.git

Usage
=====

Just replace the importing :code:`pyrallis` module with the :code:`pyrallis_plus` module in following functions.

- :code:`pyrallis.parse` -> :code:`pyrallis_plus.parse`
- :code:`@pyrallis.wrap` -> :code:`@pyrallis_plus.wrap`
- :code:`pyrallis.field` -> :code:`pyrallis_plus.field`
