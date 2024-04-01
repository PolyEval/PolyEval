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
from polyeval.target.base.value import BaseTargetValue
from polyeval.target.purescript.type import PureScriptTargetType

import json
import math


class PureScriptTargetValue(BaseTargetValue):
    def __init__(self):
        self.type = PureScriptTargetType()

    def by_null(self, vt: Type):
        return "Nothing"

    def by_bool(self, v: bool):
        return "true" if v else "false"

    def by_int(self, v: int):
        if v < 0:
            return f"({str(v)})"
        return str(v)

    def by_double(self, v: float):
        vs = "{:.7f}".format(v)[:-1]
        if vs == "-0.000000":
            vs = "0.000000"
        if vs.startswith("-"):
            return f"({vs})"
        return vs

    def by_string(self, v: str):
        return json.dumps(v)

    def by_list(self, v: list, vt: Type):
        vs_lst = [self.by(tv) for tv in v]
        vs = ", ".join(vs_lst)
        return f"[{vs}]"

    def by_ulist(self, v: list, vt: Type):
        vs_lst = [self.by(tv) for tv in v]
        vs = ", ".join(vs_lst)
        return f"[{vs}]"

    def by_idict(self, v: list[tuple], vt: Type):
        vs_lst = [f"(Tuple {self.by(k)} {self.by(v)})" for k, v in v]
        vs = ", ".join(vs_lst)
        return f"(Map.fromFoldable [{vs}])"

    def by_sdict(self, v: list[tuple], vt: Type):
        vs_lst = [f"(Tuple {self.by(k)} {self.by(v)})" for k, v in v]
        vs = ", ".join(vs_lst)
        return f"(Map.fromFoldable [{vs}])"

    def by_option(self, tv: TypedValue):
        return f"(Just {self.by(tv)})"
