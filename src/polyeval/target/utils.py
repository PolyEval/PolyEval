from __future__ import annotations

from enum import Enum


class Naming(Enum):
    SNAKE_CASE = 0
    CAMEL_CASE = 1
    PASCAL_CASE = 2
    KEBAB_CASE = 3


def get_naming_function(naming: Naming):
    def to_snake_case(snake_case_name: str):
        return snake_case_name

    def to_camel_case(snake_case_name: str):
        words = snake_case_name.split("_")
        return words[0] + "".join([word.capitalize() for word in words[1:]])

    def to_pascal_case(snake_case_name: str):
        words = snake_case_name.split("_")
        return "".join([word.capitalize() for word in words])

    def to_kebab_case(snake_case_name: str):
        return snake_case_name.replace("_", "-")

    if naming == Naming.SNAKE_CASE:
        return to_snake_case
    elif naming == Naming.CAMEL_CASE:
        return to_camel_case
    elif naming == Naming.PASCAL_CASE:
        return to_pascal_case
    elif naming == Naming.KEBAB_CASE:
        return to_kebab_case
