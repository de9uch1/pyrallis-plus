import argparse
import dataclasses
from dataclasses import _MISSING_TYPE
from logging import getLogger
from typing import Dict, List, Optional, Type, Union, cast

import pyrallis
from pyrallis.utils import Dataclass

from pyrallis_plus.wrappers.field_wrapper import FieldWrapper

logger = getLogger(__name__)


class DataclassWrapper(pyrallis.wrappers.dataclass_wrapper.DataclassWrapper):
    def __init__(
        self,
        dataclass: Type[Dataclass],
        name: Optional[str] = None,
        default: Union[Dataclass, Dict] = None,
        prefix: str = "",
        parent: "DataclassWrapper" = None,
        _field: dataclasses.Field = None,
        field_wrapper_class: Type[FieldWrapper] = FieldWrapper,
    ):
        # super().__init__(dataclass, name)
        # super().__init__(dataclass, name=name, default=default, prefix=prefix, parent=parent, _field=_field, field_wrapper_class=field_wrapper_class)
        self.dataclass = dataclass
        self._name = name
        self.default = default
        self.prefix = prefix

        self.fields: List[FieldWrapper] = []
        self._required: bool = False
        self._explicit: bool = False
        self._dest: str = ""
        self._children: List[DataclassWrapper] = []
        self._parent = parent
        # the field of the parent, which contains this child dataclass.
        self._field = _field

        # the default values
        self._defaults: List[Dataclass] = []

        if default:
            self.defaults = [default]

        self.optional: bool = False

        for field in dataclasses.fields(self.dataclass):
            if not field.init:
                continue

            elif pyrallis.utils.is_tuple_or_list_of_dataclasses(field.type):
                raise NotImplementedError(
                    f"Field {field.name} is of type {field.type}, which isn't "
                    f"supported yet. (container of a dataclass type)"
                )

            elif dataclasses.is_dataclass(field.type):
                # handle a nested dataclass attribute
                dataclass, name = field.type, field.name
                child_wrapper = DataclassWrapper(
                    dataclass,
                    name,
                    parent=self,
                    _field=field,
                    field_wrapper_class=field_wrapper_class,
                )
                self._children.append(child_wrapper)

            elif pyrallis.utils.contains_dataclass_type_arg(field.type):
                dataclass = pyrallis.utils.get_dataclass_type_arg(field.type)
                name = field.name
                child_wrapper = DataclassWrapper(
                    dataclass,
                    name,
                    parent=self,
                    _field=field,
                    default=None,
                    field_wrapper_class=field_wrapper_class,
                )
                child_wrapper.required = False
                child_wrapper.optional = True
                self._children.append(child_wrapper)

            else:
                # a normal attribute
                field_wrapper = field_wrapper_class(
                    field, parent=self, prefix=self.prefix
                )
                logger.debug(
                    f"wrapped field at {field_wrapper.dest} has a default value of {field_wrapper.default}"
                )
                self.fields.append(field_wrapper)

        logger.debug(
            f"The dataclass at attribute {self.dest} has default values: {self.defaults}"
        )
