from __future__ import annotations

from polyeval.object.function import Function
from polyeval.object.type import StringType
from polyeval.target.base.naming import BaseTargetNaming
from polyeval.target.base.type import BaseTargetType
from polyeval.target.base.value_stringify import BaseTargetValueStringify


class BaseTargetCode:
    def __init__(self):
        self.naming = BaseTargetNaming()
        self.type = BaseTargetType()
        self.stringify = BaseTargetValueStringify()
        pass

    def gen_all_signature(self, funcs: list[Function]):
        result = ""
        for func in funcs:
            result += self.gen_signature(func)
        return result

    def gen_all_self_contain(self, funcs: list[Function]):
        result = ""
        for func in funcs:
            result += self.gen_self_contain(func)
        return result

    def gen_self_contain(self, func: Function):
        func_name = self.naming.get_func_name(func.name)
        assert len(func.parameters) == 1
        assert isinstance(func.return_type, StringType)
        arg_name = self.naming.get_var_name(func.parameters[0].name)
        arg_type_str = self.type.by(func.parameters[0].type)
        return_type_str = self.type.by(func.return_type)
        return_value_str = self.stringify.get(func.parameters[0].type, arg_name)
        return self.gen_self_contain_code(
            func_name, arg_name, arg_type_str, return_type_str, return_value_str
        )

    def gen_signature(self, func: Function):
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_self_contain_code(self, func_name, arg_name, arg_type_str, return_type_str):
        raise NotImplementedError("This method must be implemented by a subclass")
