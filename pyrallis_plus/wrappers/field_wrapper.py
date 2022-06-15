from logging import getLogger
from typing import List

import pyrallis

logger = getLogger(__name__)


class FieldWrapper(pyrallis.wrappers.field_wrapper.FieldWrapper):
    """This is an extentded FieldWrapper class of Pyrallis.

    The FieldWrapper class acts a bit like an 'argparse.Action' class, which
    essentially just creates the `option_strings` and `arg_options` that get
    passed to the `add_argument(*option_strings, **arg_options)` function of the
    `argparse._ArgumentGroup` (in this case represented by the `parent`
    attribute, an instance of the class `DataclassWrapper`).

    The `option_strings`, `required`, `help`, `default`, etc.
    attributes just autogenerate the argument of the same name of the
    above-mentioned `add_argument` function. The `arg_options` attribute fills
    in the rest and may overwrite these values, depending on the type of field.

    The `field` argument is the actually wrapped `dataclasses.Field` instance.
    """

    @property
    def alias(self) -> List[str]:
        return self.field.metadata.get("alias", [])

    @property
    def option_strings(self) -> List[str]:
        """Generates the `option_strings` argument to the `add_argument` call.

        `parser.add_argument(*name_or_flags, **arg_options)`

        ## Notes:
        - Additional names for the same argument can be added via the `field`
        function.
        - Whenever the name of an attribute includes underscores ("_"), the same
        argument can be passed by using dashes ("-") instead. This also includes
        aliases.
        - If an alias contained leading dashes, either single or double, the
        same number of dashes will be used, even in the case where a prefix is
        added.

        For an illustration of this, see the aliases example.

        """

        option_strings = super().option_strings
        option_strings.extend(list(set(self.alias)))
        return option_strings