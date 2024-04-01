from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.cpp.naming import CPPTargetNaming
from polyeval.target.cpp.type import CPPTargetType
from polyeval.target.cpp.value_stringify import CPPTargetValueStringify


class CPPTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = CPPTargetNaming()
        self.type = CPPTargetType()
        self.stringify = CPPTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [
            f"{self.type.by_ref(arg.type)} {self.naming.get_var_name(arg.name)}"
            for arg in func.parameters
        ]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
{return_type} {name}({args_str}) {{
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
{return_type_str} {func_name}({arg_type_str} {arg_name}) {{
    return {ret_value_str};
}}

"""
