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


class JuliaTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return "Bool"

    def by_int(self, t: IntType):
        return "Int"

    def by_double(self, t: DoubleType):
        return "Float64"

    def by_string(self, t: StringType):
        return "String"

    def by_list(self, t: ListType):
        return f"Vector{{{self.by(t.value_type)}}}"

    def by_ulist(self, t: UListType):
        return f"Vector{{{self.by(t.value_type)}}}"

    def by_idict(self, t: IdictType):
        return f"Dict{{Int, {self.by(t.value_type)}}}"

    def by_sdict(self, t: SdictType):
        return f"Dict{{String, {self.by(t.value_type)}}}"

    def by_option(self, t: OptionType):
        return f"Union{{{self.by(t.value_type)}, Missing}}"
