from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.rust.naming import RustTargetNaming
from polyeval.target.rust.type import RustTargetType
from polyeval.target.rust.value_stringify import RustTargetValueStringify


class RustTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = RustTargetNaming()
        self.type = RustTargetType()
        self.stringify = RustTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [
            f"{self.naming.get_var_name(arg.name): {self.type.by_ref(arg.type)}}"
            for arg in func.parameters
        ]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
fn {name}({args_str}) -> {return_type} {{
    // ...
}}

"""

    def gen_self_contain(self, func: Function):
        func_name = self.naming.get_func_name(func.name)
        assert len(func.parameters) == 1
        assert isinstance(func.return_type, StringType)
        arg_name = self.naming.get_var_name(func.parameters[0].name)
        arg_type_str = self.type.by_ref(func.parameters[0].type)
        return_type_str = self.type.by(func.return_type)
        return_value_str = self.stringify.get(func.parameters[0].type, arg_name)
        return self.gen_self_contain_code(
            func_name, arg_name, arg_type_str, return_type_str, return_value_str
        )

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
fn {func_name}({arg_name}: {arg_type_str}) -> {return_type_str} {{
    {ret_value_str}
}}

"""
