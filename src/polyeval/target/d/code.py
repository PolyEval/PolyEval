from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.d.naming import DTargetNaming
from polyeval.target.d.type import DTargetType
from polyeval.target.d.value_stringify import DTargetValueStringify


class DTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = DTargetNaming()
        self.type = DTargetType()
        self.stringify = DTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [
            f"{self.type.by(arg.type)} {self.naming.get_var_name(arg.name)}"
            for arg in func.parameters
        ]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
{return_type} {name}({args_str}) {{
    // ...
}}

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
{return_type_str} {func_name}({arg_type_str} {arg_name}) {{
    return {ret_value_str};
}}

"""
