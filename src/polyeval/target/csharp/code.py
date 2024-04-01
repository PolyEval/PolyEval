from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.csharp.naming import CSharpTargetNaming
from polyeval.target.csharp.type import CSharpTargetType
from polyeval.target.csharp.value_stringify import CSharpTargetValueStringify


class CSharpTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = CSharpTargetNaming()
        self.type = CSharpTargetType()
        self.stringify = CSharpTargetValueStringify()
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
static {return_type} {name}({args_str}) {{
    // ...
}}

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
static {return_type_str} {func_name}({arg_type_str} {arg_name}) {{
    return {ret_value_str};
}}

"""
