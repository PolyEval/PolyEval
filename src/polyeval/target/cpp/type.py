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


class CPPTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_ref(self, t: Type):
        if isinstance(t, (IntType, DoubleType, BoolType)):
            return self.by(t)
        elif isinstance(
            t, (StringType, ListType, UListType, IdictType, SdictType, OptionType)
        ):
            return f"const {self.by(t)}&"
        else:
            raise ValueError(f"Unknown data type: {t}")

    def by_bool(self, t: BoolType):
        return "bool"

    def by_int(self, t: IntType):
        return "int"

    def by_double(self, t: DoubleType):
        return "double"

    def by_string(self, t: StringType):
        return "string"

    def by_list(self, t: ListType):
        return f"vector<{self.by(t.value_type)}>"

    def by_ulist(self, t: UListType):
        return f"vector<{self.by(t.value_type)}>"

    def by_idict(self, t: IdictType):
        return f"unordered_map<int, {self.by(t.value_type)}>"

    def by_sdict(self, t: SdictType):
        return f"unordered_map<string, {self.by(t.value_type)}>"

    def by_option(self, t: OptionType):
        return f"optional<{self.by(t.value_type)}>"
