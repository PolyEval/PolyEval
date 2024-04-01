from __future__ import annotations
from polyeval.object.type import Type
from polyeval.object.typed_value import TypedValue
from polyeval.dsl.node import TypeNode, ParameterNode, TestcaseNode
from polyeval.misc.utils import (
    DslValueError,
    DslParseError,
    DebugError,
    is_unrecommended_function_name,
)


class Parameter:
    def __init__(self, name: str, type: Type):
        self.name = name
        self.type = type

    def pretty_print(self):
        print(f"\t\t\t{self.name}: {self.type}")


class Testcase:
    def __init__(self, inputs: list[TypedValue], output: TypedValue):
        self.inputs = inputs
        self.output = output

    def pretty_print(self):
        inputs_str = ", ".join([str(input) for input in self.inputs])
        print(f"\t\t\t{inputs_str} -> {self.output}")


class Function:
    def __init__(
        self,
        name: str = "",
        parameters: list[Parameter] = [],
        return_type: Type = None,
        testcases: list[Testcase] = [],
    ):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.testcases = testcases

    def get_signature(self):
        args = [str(parameter.type) for parameter in self.parameters]
        args_str = ", ".join(args)
        return_type_str = str(self.return_type)
        return f"fun {self.name}({args_str}) -> {return_type_str}"

    def pretty_print(self):
        print(f"\tFunction: {self.name}")
        print(f"\t\tParameters:")
        for parameter in self.parameters:
            parameter.pretty_print()
            # print(f"\t\t\t{parameter.name}: {parameter.type}")
        print(f"\t\tReturn Type: {self.return_type}")
        print(f"\t\tTestcases:")
        for testcase in self.testcases:
            # print(f"\t\t\t{testcase.inputs} -> {testcase.output}")
            testcase.pretty_print()

    def from_node(node: FunctionNode) -> Function:
        ret = Function()
        ret.name = node.name
        if not ret.name[0].islower() or any(
            [not (c.islower() or c.isdigit() or c == "_") for c in ret.name]
        ):
            raise DslParseError(
                (node.start_line, node.start_pos),
                f"Invalid function name {ret.name}; should be lowercase letter, number or underscore and must start with a letter",
            )
        if is_unrecommended_function_name(ret.name):
            raise DslParseError(
                (node.start_line, node.start_pos),
                f"Unrecommended function name {ret.name}",
            )
        ret.parameters = [
            Parameter(param_node.name, Type.from_node(param_node.type))
            for param_node in node.parameters
        ]
        ret.return_type = Type.from_node(node.return_type)
        ret.testcases = []
        testcases = node.testcases
        for testcase_node in testcases:
            node_pos = (testcase_node.start_line, testcase_node.start_pos)
            try:
                testcase_node_inputs = testcase_node.inputs
                testcase_node_output = testcase_node.output
                testcase_types = [parameters.type for parameters in ret.parameters]
                if len(testcase_node_inputs) != len(testcase_types):
                    raise DslValueError(
                        f"Testcase expected({len(testcase_types)}) parameters, but got({len(testcase_node_inputs)})"
                    )
                input_typed_values = []
                for type, input in zip(testcase_types, testcase_node_inputs):
                    input_typed_values.append(
                        TypedValue.from_type_and_node(type, input)
                    )
                output_typed_value = TypedValue.from_type_and_node(
                    ret.return_type, testcase_node_output
                )
            except DslValueError as e:
                raise DslParseError(node_pos, e)
            ret.testcases.append(Testcase(input_typed_values, output_typed_value))
        return ret
