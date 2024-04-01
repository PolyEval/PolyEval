from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.crystal.naming import CrystalTargetNaming
from polyeval.target.crystal.type import CrystalTargetType
from polyeval.target.crystal.value_stringify import CrystalTargetValueStringify


class CrystalTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = CrystalTargetNaming()
        self.type = CrystalTargetType()
        self.stringify = CrystalTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [
            f"{self.naming.get_var_name(arg.name)} : {self.type.by(arg.type)}"
            for arg in func.parameters
        ]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
def {name}({args_str}) : {return_type}
    // ...
end

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
def {func_name}({arg_name} : {arg_type_str}) : {return_type_str}
    {ret_value_str}
end

"""
