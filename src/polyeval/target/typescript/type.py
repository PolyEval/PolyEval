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


class TypeScriptTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return "boolean"

    def by_int(self, t: IntType):
        return "number"

    def by_double(self, t: DoubleType):
        return "number"

    def by_string(self, t: StringType):
        return "string"

    def by_list(self, t: ListType):
        return f"{self.by(t.value_type)}[]"

    def by_ulist(self, t: UListType):
        return f"{self.by(t.value_type)}[]"

    def by_idict(self, t: IdictType):
        return f"Map<number,{self.by(t.value_type)}>"

    def by_sdict(self, t: SdictType):
        return f"Map<string,{self.by(t.value_type)}>"

    def by_option(self, t: OptionType):
        return f"({self.by(t.value_type)} | null)"
