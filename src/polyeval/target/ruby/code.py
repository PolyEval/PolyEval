from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.ruby.naming import RubyTargetNaming
from polyeval.target.ruby.type import RubyTargetType
from polyeval.target.ruby.value_stringify import RubyTargetValueStringify


class RubyTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = RubyTargetNaming()
        self.type = RubyTargetType()
        self.stringify = RubyTargetValueStringify()
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
def {name}({args_str})
    // ...
end

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
def {func_name}({arg_name})
    {ret_value_str}
end

"""
