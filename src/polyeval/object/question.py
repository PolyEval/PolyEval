from __future__ import annotations
from polyeval.object.function import Function
from polyeval.dsl.node import QuestionNode
from polyeval.dsl.parsing import parse


class Question:
    def __init__(self, name: str = "", functions: list[Function] = []):
        self.name = name
        self.functions = functions

    def pretty_print(self):
        print(f"Question: {self.name}")
        for function in self.functions:
            function.pretty_print()

    def from_node(node: QuestionNode) -> Question:
        question_name = node.name
        if not question_name.isidentifier():
            raise DslParseError(
                (node.start_line, node.start_pos),
                f"Invalid question name {question_name}; should be identifier",
            )
        question_functions = [
            Function.from_node(func_node) for func_node in node.functions
        ]
        return Question(question_name, question_functions)


def parse_questions(s: str) -> list[Question]:
    return [Question.from_node(node) for node in parse(s)]
