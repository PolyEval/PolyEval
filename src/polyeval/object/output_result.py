from __future__ import annotations
from polyeval.object.function import Function
from polyeval.object.type import Type
from polyeval.object.typed_value import TypedValue
from polyeval.dsl.node import OutFunctionNode, OutTestcaseNode
from polyeval.dsl.parsing import parse_output


class OutTestcase:
    def __init__(
        self,
        inputs: list[TypedValue],
        output: TypedValue,
        expected: TypeValue,
        side_effects: list[TypedValue],
    ):
        self.inputs = inputs
        self.output = output
        self.expected = expected
        self.side_effects = side_effects

    def pretty_print(self):
        inputs_str = ", ".join([str(i) for i in self.inputs])
        side_effects_str = ", ".join(
            [str(side_effect) for side_effect in self.side_effects]
        )
        print(f"\t\t-")
        print(f"\t\t({inputs_str}) -> {self.output}")
        print(f"\t\texpected: {self.expected}")
        print(f"\t\tside effects: ({side_effects_str})")

    def is_no_side_effect(self) -> bool:
        for before, after in zip(self.inputs, self.side_effects):
            if str(before) != str(after):
                return False
        return True

    def is_expected(self) -> bool:
        return str(self.output) == str(self.expected)


class OutFunction:
    def __init__(
        self,
        name: str = "",
        param_types: list[Type] = [],
        return_type: Type = None,
        testcases: list[OutTestcase] = [],
    ):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type
        self.testcases = testcases

    def pretty_print(self):
        params_str = "(" + ", ".join([str(t) for t in self.param_types]) + ")"
        print(f"Function: {self.name}")
        print(f"\tParameters: {params_str}")
        print(f"\tReturn Type: {self.return_type}")
        print(f"\tTestcases:")
        for testcase in self.testcases:
            testcase.pretty_print()

    def from_node(node: OutFunctionNode) -> OutFunction:
        ret = OutFunction()
        ret.name = node.name
        if not ret.name[0].islower() or any(
            [not (c.islower() or c.isdigit() or c == "_") for c in ret.name]
        ):
            raise DslParseError(
                (node.start_line, node.start_pos),
                f"Invalid function name {ret.name}; should be lowercase letter, number or underscore and must start with a letter",
            )
        ret.param_types = [
            Type.from_node(param_node) for param_node in node.param_types
        ]
        ret.return_type = Type.from_node(node.return_type)
        ret.testcases = []
        for testcase_node in node.testcases:
            node_pos = (testcase_node.start_line, testcase_node.start_pos)
            try:
                testcase_node_inputs = testcase_node.inputs
                testcase_node_output = testcase_node.output
                testcase_node_expected = testcase_node.expected
                testcase_node_side_effects = testcase_node.side_effects
                testcase_types = ret.param_types
                if len(testcase_node_inputs) != len(testcase_types):
                    raise DslValueError(
                        f"Expected {len(testcase_types)} inputs, got {len(testcase_node_inputs)}"
                    )
                if len(testcase_node_side_effects) != len(testcase_types):
                    raise DslValueError(
                        f"Expected {len(testcase_types)} side effects, got {len(testcase_node_side_effects)}"
                    )
                input_typed_values = []
                for i in range(len(testcase_node_inputs)):
                    input_typed_values.append(
                        TypedValue.from_type_and_node(
                            testcase_types[i], testcase_node_inputs[i]
                        )
                    )
                side_effect_typed_values = []
                for i in range(len(testcase_node_side_effects)):
                    side_effect_typed_values.append(
                        TypedValue.from_type_and_node(
                            testcase_types[i], testcase_node_side_effects[i]
                        )
                    )
                output_typed_value = TypedValue.from_type_and_node(
                    ret.return_type, testcase_node_output
                )
                expected_typed_value = TypedValue.from_type_and_node(
                    ret.return_type, testcase_node_expected
                )
            except DslValueError as e:
                raise DslParseError(node_pos, str(e))
            ret.testcases.append(
                OutTestcase(
                    input_typed_values,
                    output_typed_value,
                    expected_typed_value,
                    side_effect_typed_values,
                )
            )
        return ret

    def is_no_side_effect(self) -> bool:
        for testcase in self.testcases:
            if not testcase.is_no_side_effect():
                return False
        return True

    def is_expected(self) -> bool:
        for testcase in self.testcases:
            if not testcase.is_expected():
                return False
        return True


def parse_result(s: str) -> list[Question]:
    return [OutFunction.from_node(node) for node in parse_output(s)]
