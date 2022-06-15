import dataclasses
from typing import List, Optional, Union

import pyrallis


def field(
    *,
    default=dataclasses.MISSING,
    default_factory=dataclasses.MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
    is_mutable=False,
    alias: Optional[Union[List[str], str]] = None,
) -> dataclasses.Field:

    if alias is not None:
        _metadata = {"alias": [alias] if isinstance(alias, str) else alias}
        if metadata is not None:
            metadata.update(_metadata)
        else:
            metadata = _metadata

    return pyrallis.fields.field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        is_mutable=is_mutable,
    )
