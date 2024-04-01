from __future__ import annotations

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


class BaseTargetType:
    def __init__(self):
        pass

    def by(self, t: Type):
        if isinstance(t, IntType):
            return self.by_int(t)
        if isinstance(t, DoubleType):
            return self.by_double(t)
        if isinstance(t, BoolType):
            return self.by_bool(t)
        if isinstance(t, StringType):
            return self.by_string(t)
        if isinstance(t, ListType):
            return self.by_list(t)
        if isinstance(t, UListType):
            return self.by_ulist(t)
        if isinstance(t, IdictType):
            return self.by_idict(t)
        if isinstance(t, SdictType):
            return self.by_sdict(t)
        if isinstance(t, OptionType):
            return self.by_option(t)
        else:
            raise ValueError(f"Unknown data type: {t}")

    def by_bool(self, t: BoolType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_int(self, t: IntType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_double(self, t: DoubleType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_string(self, t: StringType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_list(self, t: ListType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_ulist(self, t: UListType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_idict(self, t: IdictType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_sdict(self, t: SdictType):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_option(self, t: OptionType):
        raise NotImplementedError("This method must be implemented by a subclass")
