import pyrallis
from pyrallis import ParsingError, decode, dump, encode, load

from pyrallis_plus.argparsing import ArgumentParser, parse, wrap
from pyrallis_plus.fields import field

def __replace(module, name, new_obj):
    orig = getattr(module, name, None)
    setattr(module, "__orig_" + name, orig)
    setattr(module, name, new_obj)

__replace(pyrallis, "ArgumentParser", ArgumentParser)
__replace(pyrallis, "parse", parse)
__replace(pyrallis, "wrap", wrap)
__replace(pyrallis, "field", field)
