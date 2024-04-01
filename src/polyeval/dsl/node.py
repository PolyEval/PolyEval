from __future__ import annotations


class Node:
    def __init__(self, start_line: int, start_pos: int):
        self.start_line = start_line
        self.start_pos = start_pos


class TypeNode(Node):
    def __init__(self, start_line: int, start_pos: int, type_name: str):
        super().__init__(start_line, start_pos)
        self.type_name = type_name


class VTypeNode(TypeNode):
    def __init__(
        self, start_line: int, start_pos: int, type_name: str, value_type: TypeNode
    ):
        super().__init__(start_line, start_pos, type_name)
        self.value_type = value_type


class KVTypeNode(VTypeNode):
    def __init__(
        self,
        start_line: int,
        start_pos: int,
        type_name: str,
        key_type: TypeNode,
        value_type: TypeNode,
    ):
        super().__init__(start_line, start_pos, type_name, value_type)
        self.key_type = key_type


class ValueNode(Node):
    def __init__(self, start_line: int, start_pos: int, val):
        super().__init__(start_line, start_pos)
        self.value = val


class QuestionNode(Node):
    def __init__(
        self,
        start_line: int,
        start_pos: int,
        question_name: str,
        functions: list[FunctionNode],
    ):
        super().__init__(start_line, start_pos)
        self.name = question_name
        self.functions = functions


class FunctionNode(Node):
    def __init__(
        self,
        start_line: int,
        start_pos: int,
        function_name: str,
        parameters: list[ParameterNode],
        return_type: TypeNode,
        testcases: list[TestcaseNode],
    ):
        super().__init__(start_line, start_pos)
        self.name = function_name
        self.parameters = parameters
        self.return_type = return_type
        self.testcases = testcases


class ParameterNode(Node):
    def __init__(self, start_line: int, start_pos: int, name: str, type: TypeNode):
        super().__init__(start_line, start_pos)
        self.name = name
        self.type = type


class TestcaseNode(Node):
    def __init__(
        self,
        start_line: int,
        start_pos: int,
        inputs: list[ValueNode],
        output: ValueNode,
    ):
        super().__init__(start_line, start_pos)
        self.inputs = inputs
        self.output = output


class OutFunctionNode(Node):
    def __init__(
        self,
        start_line: int,
        start_pos: int,
        function_name: str,
        param_types: list[TypeNode],
        return_type: TypeNode,
        testcases: list[OutTestcaseNode],
    ):
        super().__init__(start_line, start_pos)
        self.name = function_name
        self.param_types = param_types
        self.return_type = return_type
        self.testcases = testcases


class OutTestcaseNode(Node):
    def __init__(
        self,
        start_line: int,
        start_pos: int,
        inputs: list[ValueNode],
        output: ValueNode,
        expected: ValueNode,
        side_effects: list[ValueNode],
    ):
        super().__init__(start_line, start_pos)
        self.inputs = inputs
        self.output = output
        self.expected = expected
        self.side_effects = side_effects
