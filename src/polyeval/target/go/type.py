from __future__ import annotations
from polyeval.target.base.type import BaseTargetType
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


class GoTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return "bool"

    def by_int(self, t: IntType):
        return "int"

    def by_double(self, t: DoubleType):
        return "float64"

    def by_string(self, t: StringType):
        return "string"

    def by_list(self, t: ListType):
        return f"[]{self.by(t.value_type)}"

    def by_ulist(self, t: UListType):
        return f"[]{self.by(t.value_type)}"

    def by_idict(self, t: IdictType):
        return f"map[int]{self.by(t.value_type)}"

    def by_sdict(self, t: SdictType):
        return f"map[string]{self.by(t.value_type)}"

    def by_option(self, t: OptionType):
        return f"*{self.by(t.value_type)}"
