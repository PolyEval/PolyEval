from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.hack.naming import HackTargetNaming
from polyeval.target.hack.type import HackTargetType
from polyeval.target.hack.value_stringify import HackTargetValueStringify


class HackTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = HackTargetNaming()
        self.type = HackTargetType()
        self.stringify = HackTargetValueStringify()
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
function {name}({args_str}): {return_type} {{
    // ...
}}

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
function {func_name}({arg_type_str} {arg_name}): {return_type_str} {{
    return {ret_value_str};
}}

"""
