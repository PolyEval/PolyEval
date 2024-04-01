from __future__ import annotations

from polyeval.object.function import Function
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.elixir.naming import ElixirTargetNaming
from polyeval.target.elixir.type import ElixirTargetType
from polyeval.target.elixir.value_stringify import ElixirTargetValueStringify


class ElixirTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = ElixirTargetNaming()
        self.type = ElixirTargetType()
        self.stringify = ElixirTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [f"{self.naming.get_var_name(arg.name)}" for arg in func.parameters]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
def {name}({args_str}) do
    # ...
end

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
def {func_name}({arg_name}) do
    {ret_value_str}
end

"""
