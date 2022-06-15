Pyrallis+
#########

This is an enhanced `pyrallis <https://github.com/eladrich/pyrallis>`_, dataclass-based simple configuration library.

`Pyrallis <https://github.com/eladrich/pyrallis>`_ is an awesome configuration library based on the python dataclass.
It is designed to be a simple and clean library.
This extended library adds some features to Pyrallis at the expense of simplicity.

The extended features are as follows:

- :code:`-h` option: the short option of :code:`--help`
- Command-line option alias:

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
