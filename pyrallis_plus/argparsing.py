"""Simple, Elegant Argument parsing.
@author: Fabrice Normandin
"""
import argparse
import dataclasses
import inspect
import sys
import warnings
from argparse import HelpFormatter, Namespace
from collections import defaultdict
from functools import wraps
from itertools import chain
from logging import getLogger
from pathlib import Path
from typing import Dict, Generic, List, Optional, Sequence, Text, Type, TypeVar, Union

import pyrallis
from pyrallis import cfgparsing, utils
from pyrallis.parsers import decoding
from pyrallis.utils import Dataclass, PyrallisException

from pyrallis_plus.help_formatter import SimpleHelpFormatter
from pyrallis_plus.wrappers.dataclass_wrapper import DataclassWrapper
from pyrallis_plus.wrappers.field_wrapper import FieldWrapper

logger = getLogger(__name__)

T = TypeVar("T")


class ArgumentParser(pyrallis.argparsing.ArgumentParser, Generic[T]):
    """Extended `pyrallis.argparsing.ArgumentParser` class."""

    def __init__(
        self,
        config_class: Type[T],
        config_path: Optional[str] = None,
        formatter_class: Type[HelpFormatter] = SimpleHelpFormatter,
        *args,
        **kwargs,
    ):
        super().__init__(
            config_class,
            config_path=config_path,
            formatter_class=formatter_class,
            *args,
            **kwargs,
        )

    def set_dataclass(
        self,
        dataclass: Union[Type[Dataclass], Dataclass],
        prefix: str = "",
        default: Union[Dataclass, Dict] = None,
        dataclass_wrapper_class: Type[DataclassWrapper] = DataclassWrapper,
    ):
        """Adds command-line arguments for the fields of `dataclass`."""
        if not isinstance(dataclass, type):
            default = dataclass if default is None else default
            dataclass = type(dataclass)

        new_wrapper = dataclass_wrapper_class(
            dataclass, prefix=prefix, default=default, field_wrapper_class=FieldWrapper
        )
        self._wrappers.append(new_wrapper)
        self._wrappers += new_wrapper.descendants

        for wrapper in self._wrappers:
            logger.debug(
                f"Adding arguments for dataclass: {wrapper.dataclass} "
                f"at destination {wrapper.dest}"
            )
            wrapper.add_arguments(parser=self)

    def parse_known_args(
        self,
        args: Sequence[Text] = None,
        namespace: Namespace = None,
        attempt_to_reorder: bool = False,
    ):
        # NOTE: since the usual ArgumentParser.parse_args() calls
        # parse_known_args, we therefore just need to overload the
        # parse_known_args method to support both.
        if args is None:
            # args default to the system args
            args = sys.argv[1:]
        else:
            # make sure that args are mutable
            args = list(args)

        help_args = set(
            chain.from_iterable(
                [
                    action.option_strings
                    for action in self._actions
                    if isinstance(action, argparse._HelpAction)
                ]
            )
        )
        if all(help_arg not in args for help_arg in help_args):
            for action in self._actions:
                # TODO: Find a better way to do that?
                action.default = (
                    argparse.SUPPRESS
                )  # To avoid setting of defaults in actual run
                action.type = (
                    str  # In practice, we want all processing to happen with yaml
                )
        parsed_args, unparsed_args = super(
            pyrallis.argparsing.ArgumentParser, self
        ).parse_known_args(args, namespace)

        # for action="store_true"
        parsed_args = Namespace(
            **{name: str(arg) for name, arg in vars(parsed_args).items()}
        )

        parsed_args = self._postprocessing(parsed_args)
        return parsed_args, unparsed_args


def parse(
    config_class: Type[T],
    config_path: Optional[Union[Path, str]] = None,
    args: Optional[Sequence[str]] = None,
) -> T:
    parser = ArgumentParser(config_class=config_class, config_path=config_path)
    return parser.parse_args(args)


def wrap(config_path=None):
    def wrapper_outer(fn):
        @wraps(fn)
        def wrapper_inner(*args, **kwargs):
            argspec = inspect.getfullargspec(fn)
            argtype = argspec.annotations[argspec.args[0]]
            cfg = parse(config_class=argtype, config_path=config_path)
            response = fn(cfg, *args, **kwargs)
            return response

        return wrapper_inner

    return wrapper_outer
