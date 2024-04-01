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


class ObjectiveCTargetValueStringify(BaseTargetValueStringify):
    def __init__(self):
        pass

    def by_bool(self):
        return "[self p_e_bool]"

    def by_int(self):
        return "[self p_e_int]"

    def by_double(self):
        return "[self p_e_double]"

    def by_string(self):
        return "[self p_e_string]"

    def by_list(self, value_type: Type):
        return f"[self p_e_list:{self.by(value_type)}]"

    def by_ulist(self, value_type: Type):
        return f"[self p_e_ulist:{self.by(value_type)}]"

    def by_idict(self, value_type: Type):
        return f"[self p_e_idict:{self.by(value_type)}]"

    def by_sdict(self, value_type: Type):
        return f"[self p_e_sdict:{self.by(value_type)}]"

    def by_option(self, value_type: Type):
        return f"[self p_e_option:{self.by(value_type)}]"

    def apply(self, stringifier_str: str, value_str: str):
        return f"{stringifier_str}({value_str})"
