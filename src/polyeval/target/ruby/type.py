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


class RubyTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return ""

    def by_int(self, t: IntType):
        return ""

    def by_double(self, t: DoubleType):
        return ""

    def by_string(self, t: StringType):
        return ""

    def by_list(self, t: ListType):
        return f""

    def by_ulist(self, t: UListType):
        return f""

    def by_idict(self, t: IdictType):
        return f""

    def by_sdict(self, t: SdictType):
        return f""

    def by_option(self, t: OptionType):
        return f""
