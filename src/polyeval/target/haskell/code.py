from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.haskell.naming import HaskellTargetNaming
from polyeval.target.haskell.type import HaskellTargetType
from polyeval.target.haskell.value_stringify import HaskellTargetValueStringify


class HaskellTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = HaskellTargetNaming()
        self.type = HaskellTargetType()
        self.stringify = HaskellTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args_type = [self.type.by(arg.type) for arg in func.parameters]
        args_type_str = " -> ".join(args_type)
        args = [f"{self.naming.get_var_name(arg.name)}" for arg in func.parameters]
        args_str = " ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
{name} :: {args_type_str} -> {return_type}
{name} {args_str} =
    -- ...

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
{func_name} :: {arg_type_str} -> {return_type_str}
{func_name} {arg_name} =
    {ret_value_str}

"""
