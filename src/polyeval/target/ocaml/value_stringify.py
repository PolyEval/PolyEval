from __future__ import annotations

from polyeval.object.type import (
    Type,
    IntType,
    DoubleType,
    BoolType,
    StringType,
    ListType,
    UListType,
    IdictType,
    SdictType,
    OptionType,
)
from polyeval.target.base.value_stringify import *


class OCamlTargetValueStringify(MLTargetValueStringify):
    def __init__(self):
        pass

    def apply(self, stringifier_str: str, value_str: str):
        return f"({stringifier_str} {value_str})"
