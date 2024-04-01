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


class CrystalTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return "Bool"

    def by_int(self, t: IntType):
        return "Int32"

    def by_double(self, t: DoubleType):
        return "Float64"

    def by_string(self, t: StringType):
        return "String"

    def by_list(self, t: ListType):
        return f"Array({self.by(t.value_type)})"

    def by_ulist(self, t: UListType):
        return f"Array({self.by(t.value_type)})"

    def by_idict(self, t: IdictType):
        return f"Hash(Int32, {self.by(t.value_type)})"

    def by_sdict(self, t: SdictType):
        return f"Hash(String, {self.by(t.value_type)})"

    def by_option(self, t: OptionType):
        return f"({self.by(t.value_type)} | Nil)"
