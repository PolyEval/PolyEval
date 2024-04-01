from __future__ import annotations

from polyeval.object.function import Function
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.python.naming import PythonTargetNaming
from polyeval.target.python.type import PythonTargetType
from polyeval.target.python.value_stringify import PythonTargetValueStringify


class PythonTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = PythonTargetNaming()
        self.type = PythonTargetType()
        self.stringify = PythonTargetValueStringify()
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
def {name}({args_str}) -> {return_type}:
    # ...

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
def {func_name}({arg_name}: {arg_type_str}) -> {return_type_str}:
    return {ret_value_str}

"""
