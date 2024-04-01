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


class BaseTargetValueStringify:
    def __init__(self):
        pass

    def get(self, t: Type, value_str: str):
        stringifier = self.by(t)
        return self.apply(stringifier, value_str)

    def by(self, t: Type):
        if isinstance(t, IntType):
            return self.by_int()
        if isinstance(t, DoubleType):
            return self.by_double()
        if isinstance(t, BoolType):
            return self.by_bool()
        if isinstance(t, StringType):
            return self.by_string()
        if isinstance(t, ListType):
            return self.by_list(t.value_type)
        if isinstance(t, UListType):
            return self.by_ulist(t.value_type)
        if isinstance(t, IdictType):
            return self.by_idict(t.value_type)
        if isinstance(t, SdictType):
            return self.by_sdict(t.value_type)
        if isinstance(t, OptionType):
            return self.by_option(t.value_type)
        raise ValueError(f"Unknown data type: {t}")

    def by_bool(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_int(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_double(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_string(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_list(self, value_type: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_ulist(self, value_type: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_idict(self, value_type: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_sdict(self, value_type: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def by_option(self, value_type: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def apply(self, stringifier: str, value_str: str):
        raise NotImplementedError("This method must be implemented by a subclass")


class CommonTargetValueStringify(BaseTargetValueStringify):
    def __init__(self):
        pass

    def by_bool(self):
        return "p_e_bool()"

    def by_int(self):
        return "p_e_int()"

    def by_double(self):
        return "p_e_double()"

    def by_string(self):
        return "p_e_string()"

    def by_list(self, value_type: Type):
        return f"p_e_list({self.by(value_type)})"

    def by_ulist(self, value_type: Type):
        return f"p_e_ulist({self.by(value_type)})"

    def by_idict(self, value_type: Type):
        return f"p_e_idict({self.by(value_type)})"

    def by_sdict(self, value_type: Type):
        return f"p_e_sdict({self.by(value_type)})"

    def by_option(self, value_type: Type):
        return f"p_e_option({self.by(value_type)})"


class LispTargetValueStringify(BaseTargetValueStringify):
    def __init__(self):
        pass

    def by_bool(self):
        return "(p_e_bool)"

    def by_int(self):
        return "(p_e_int)"

    def by_double(self):
        return "(p_e_double)"

    def by_string(self):
        return "(p_e_string)"

    def by_list(self, value_type: Type):
        return f"(p_e_list {self.by(value_type)})"

    def by_ulist(self, value_type: Type):
        return f"(p_e_ulist {self.by(value_type)})"

    def by_idict(self, value_type: Type):
        return f"(p_e_idict {self.by(value_type)})"

    def by_sdict(self, value_type: Type):
        return f"(p_e_sdict {self.by(value_type)})"

    def by_option(self, value_type: Type):
        return f"(p_e_option {self.by(value_type)})"


class MLTargetValueStringify(BaseTargetValueStringify):
    def __init__(self):
        pass

    def by_bool(self):
        return "p_e_bool"

    def by_int(self):
        return "p_e_int"

    def by_double(self):
        return "p_e_double"

    def by_string(self):
        return "p_e_string"

    def by_list(self, value_type: Type):
        return f"(p_e_list {self.by(value_type)})"

    def by_ulist(self, value_type: Type):
        return f"(p_e_ulist {self.by(value_type)})"

    def by_idict(self, value_type: Type):
        return f"(p_e_idict {self.by(value_type)})"

    def by_sdict(self, value_type: Type):
        return f"(p_e_sdict {self.by(value_type)})"

    def by_option(self, value_type: Type):
        return f"(p_e_option {self.by(value_type)})"
