from __future__ import annotations

import copy
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
from polyeval.object.typed_value import TypedValue
from polyeval.target.base.type import BaseTargetType


class BaseTargetValue:
    def __init__(self):
        self.type = BaseTargetType()

    def by(self, tv: TypedValue):
        t, v = tv.type, tv.value
        if isinstance(t, OptionType):
            if v == None:
                return self.by_null(t.value_type)
            else:
                new_tv = copy.deepcopy(tv)
                new_tv.type = t.value_type
                return self.by_option(new_tv)
        return self.by_non_option(tv)

    def by_non_option(self, tv: TypedValue):
        t, v = tv.type, tv.value
        if isinstance(t, IntType):
            return self.by_int(v)
        if isinstance(t, DoubleType):
            return self.by_double(v)
        if isinstance(t, BoolType):
            return self.by_bool(v)
        if isinstance(t, StringType):
            return self.by_string(v)
        if isinstance(t, ListType):
            return self.by_list(v, t.value_type)
        if isinstance(t, UListType):
            return self.by_ulist(v, t.value_type)
        if isinstance(t, IdictType):
            return self.by_idict(v, t.value_type)
        if isinstance(t, SdictType):
            return self.by_sdict(v, t.value_type)
        else:
            raise ValueError(f"Unknown data type: {t}")

    def by_null(self, vt: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_bool(self, v: bool):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_int(self, v: int):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_double(self, v: float):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_string(self, v: str):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_list(self, v: list, vt: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_ulist(self, v: list, vt: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_idict(self, v: list[tuple], vt: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_sdict(self, v: list[tuple], vt: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_option(self, tv: TypedValue):
        raise NotImplementedError("This method must be implemented by a subclass")
