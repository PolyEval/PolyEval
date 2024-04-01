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


class ObjectiveCTargetType(BaseTargetType):
    def __init__(self):
        pass

    def by_bool(self, t: BoolType):
        return "NSNumber *"

    def by_int(self, t: IntType):
        return "NSNumber *"

    def by_double(self, t: DoubleType):
        return "NSNumber *"

    def by_string(self, t: StringType):
        return "NSString *"

    def by_list(self, t: ListType):
        return f"NSArray<{self.by(t.value_type)}> *"

    def by_ulist(self, t: UListType):
        return f"NSArray<{self.by(t.value_type)}> *"

    def by_idict(self, t: IdictType):
        return f"NSDictionary<NSNumber *, {self.by(t.value_type)}> *"

    def by_sdict(self, t: SdictType):
        return f"NSDictionary<NSString *, {self.by(t.value_type)}> *"

    def by_option(self, t: OptionType):
        return f"{self.by(t.value_type)}"
