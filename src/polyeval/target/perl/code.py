from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.code import BaseTargetCode
from polyeval.target.perl.naming import PerlTargetNaming
from polyeval.target.perl.type import PerlTargetType
from polyeval.target.perl.value_stringify import PerlTargetValueStringify


class PerlTargetCode(BaseTargetCode):
    def __init__(self):
        self.naming = PerlTargetNaming()
        self.type = PerlTargetType()
        self.stringify = PerlTargetValueStringify()
        pass

    def gen_signature(self, func: Function):
        name = self.naming.get_func_name(func.name)
        args = [f"{self.naming.get_var_name(arg.name)}" for arg in func.parameters]
        args_str = ", ".join(args)
        return_type = self.type.by(func.return_type)
        return f"""\
sub {name}({args_str}) {{
    # ...
}}

"""

    def gen_self_contain_code(
        self, func_name, arg_name, arg_type_str, return_type_str, ret_value_str
    ):
        return f"""\
sub {func_name}({arg_name}) {{
    return {ret_value_str};
}}

"""
