import pyrallis


class SimpleHelpFormatter(pyrallis.help_formatter.SimpleHelpFormatter):
    """Extended `pyrallis.help_formatter.SimpleHelpFormatter` class.

    Little shorthand for using some useful HelpFormatters from argparse.

    This class inherits from argparse's `ArgumentDefaultHelpFormatter`,
    `MetavarTypeHelpFormatter` and `RawDescriptionHelpFormatter` classes.

    This produces the following resulting actions:
    - adds a "(default: xyz)" for each argument with a default
    - uses the name of the argument type as the metavar. For example, gives
      "-n int" instead of "-n N" in the usage and description of the arguments.
    - Conserves the format of the class and argument docstrings, if given.
    """

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        else:

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                return ", ".join(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                return ", ".join(action.option_strings) + " " + args_string


Formatter = SimpleHelpFormatter
