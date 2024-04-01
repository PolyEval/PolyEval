from __future__ import annotations

import copy
from polyeval.misc.utils import add_indent
from polyeval.object.function import Function, Parameter, Testcase
from polyeval.object.type import (
    Type,
    IntType,
    DoubleType,
    BoolType,
    StringType,
    ListType,
    UListType,
    IdictType,
    SdictType,
    OptionType,
)
from polyeval.object.typed_value import TypedValue
from polyeval.target.base.type import BaseTargetType
from polyeval.target.base.naming import BaseTargetNaming
from polyeval.target.base.value import BaseTargetValue
from polyeval.target.base.value_stringify import BaseTargetValueStringify
import json


class BaseTargetTests:
    def __init__(self):
        self.naming = BaseTargetNaming()
        self.type = BaseTargetType()
        self.value = BaseTargetValue()
        self.stingify = BaseTargetValueStringify()
        pass

    def gen_code(self, funcs: list[Function]) -> str:
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_all_tests(
        self, funcs: list[Function]
    ) -> list(tuple[str, list[tuple[str, str]]]):
        result = []
        for func in funcs:
            result.append(self.gen_function_all_tests(func))
        return result

    def gen_function_all_tests(
        self, func: Function
    ) -> tuple[str, list[tuple[str, str]]]:
        func_name = func.name
        func_params = func.parameters
        func_ret_type = func.return_type
        func_tests = func.testcases
        result = []
        for idx, testcase in enumerate(func_tests):
            result.append(
                self.gen_function_test(
                    func_name, idx, func_params, func_ret_type, testcase
                )
            )
        return (func.get_signature(), result)

    def gen_function_test(
        self,
        func_name: str,
        idx: int,
        func_params: list[Parameter],
        func_ret_type: Type,
        func_test: Testcase,
    ) -> tuple[str, str]:
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_assign_vars_cmds(
        self, params_names: list[str], test_inputs: list[TypedValue]
    ):
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_input_str_cmd(self, params_names: list[str], input_types: list[Type]):
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_side_str_cmd(self, params_names: list[str], input_types: list[Type]):
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_output_cmd(self, func_name: str, params_names: list[str]):
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_output_str_cmd(self, type: Type):
        raise NotImplementedError("This method must be implemented by a subclass")

    def gen_expected_str_cmd(self, value: TypedValue):
        raise NotImplementedError("This method must be implemented by a subclass")
