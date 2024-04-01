from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.kotlin.naming import KotlinTargetNaming
from polyeval.target.kotlin.type import KotlinTargetType
from polyeval.target.kotlin.value_stringify import KotlinTargetValueStringify


class KotlinTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = KotlinTargetNaming()
        self.type = KotlinTargetType()
        self.stringify = KotlinTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [
            f"{self.naming.get_var_name(arg.name)}: {self.type.by(arg.type)}"
            for arg in func.parameters
        ]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
fun {name}({args_str}): {return_type} {{
    // ...
}}

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
fun {func_name}({arg_name}: {arg_type_str}): {return_type_str} {{
    return {ret_value_str}
}}

"""
