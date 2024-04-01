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


class ScalaTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return "Boolean"

    def by_int(self, t: IntType):
        return "Int"

    def by_double(self, t: DoubleType):
        return "Double"

    def by_string(self, t: StringType):
        return "String"

    def by_list(self, t: ListType):
        return f"Seq[{self.by(t.value_type)}]"

    def by_ulist(self, t: UListType):
        return f"Seq[{self.by(t.value_type)}]"

    def by_idict(self, t: IdictType):
        return f"Map[Int, {self.by(t.value_type)}]"

    def by_sdict(self, t: SdictType):
        return f"Map[String, {self.by(t.value_type)}]"

    def by_option(self, t: OptionType):
        return f"Option[{self.by(t.value_type)}]"
