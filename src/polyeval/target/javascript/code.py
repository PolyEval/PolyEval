from __future__ import annotations

from polyeval.object.function import Function
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.javascript.naming import JavaScriptTargetNaming
from polyeval.target.javascript.type import JavaScriptTargetType
from polyeval.target.javascript.value_stringify import JavaScriptTargetValueStringify


class JavaScriptTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = JavaScriptTargetNaming()
        self.type = JavaScriptTargetType()
        self.stringify = JavaScriptTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [f"{self.naming.get_var_name(arg.name)}" for arg in func.parameters]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
function {name}({args_str}) {{
    // ...
}}

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
function {func_name}({arg_name}) {{
    return {ret_value_str};
}}

"""
