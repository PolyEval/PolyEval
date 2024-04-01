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


class RustTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_ref(self, t: Type):
        if isinstance(t, (IntType, DoubleType, BoolType)):
            return self.by(t)
        elif isinstance(
            t, (StringType, ListType, UListType, IdictType, SdictType, OptionType)
        ):
            return f"&{self.by(t)}"
        else:
            raise ValueError(f"Unknown data type: {t}")

    def by_bool(self, t: BoolType):
        return "bool"

    def by_int(self, t: IntType):
        return "i32"

    def by_double(self, t: DoubleType):
        return "f64"

    def by_string(self, t: StringType):
        return "String"

    def by_list(self, t: ListType):
        return f"Vec<{self.by(t.value_type)}>"

    def by_ulist(self, t: UListType):
        return f"Vec<{self.by(t.value_type)}>"

    def by_idict(self, t: IdictType):
        return f"HashMap<i32, {self.by(t.value_type)}>"

    def by_sdict(self, t: SdictType):
        return f"HashMap<String, {self.by(t.value_type)}>"

    def by_option(self, t: OptionType):
        return f"Option<{self.by(t.value_type)}>"
