from __future__ import annotations

from polyeval.object.function import Function
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.lua.naming import LuaTargetNaming
from polyeval.target.lua.type import LuaTargetType
from polyeval.target.lua.value_stringify import LuaTargetValueStringify


class LuaTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = LuaTargetNaming()
        self.type = LuaTargetType()
        self.stringify = LuaTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [f"{self.naming.get_var_name(arg.name)}" for arg in func.parameters]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
function {name}({args_str})
    // ...
end

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
function {func_name}({arg_name})
    return {ret_value_str}
end

"""
