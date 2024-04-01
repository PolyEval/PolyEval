from __future__ import annotations
from polyeval.dsl.node import TypeNode, VTypeNode, KVTypeNode, ValueNode
from polyeval.misc.utils import DslValueError, DslParseError, DebugError
from polyeval.object.type import (
    Type,
    BoolType,
    IntType,
    DoubleType,
    StringType,
    ListType,
    UListType,
    IdictType,
    SdictType,
    OptionType,
)
import json


class TypedValue:
    def __init__(self, type: Type, value: Any):
        self.type: Type = type
        self.value: Any = value
        self.parent: TypedValue = None

    def get_value_str(self) -> str:
        if isinstance(self.type, OptionType) and self.value is None:
            return "null"
        elif isinstance(self.type, BoolType) or (
            isinstance(self.type, OptionType)
            and isinstance(self.type.value_type, BoolType)
        ):
            return "true" if self.value else "false"
        elif isinstance(self.type, IntType) or (
            isinstance(self.type, OptionType)
            and isinstance(self.type.value_type, IntType)
        ):
            return str(self.value)
        elif isinstance(self.type, DoubleType) or (
            isinstance(self.type, OptionType)
            and isinstance(self.type.value_type, DoubleType)
        ):
            if self.value == float("inf"):
                raise DebugError("`inf` is not supported")
                # return "inf"
            elif self.value == float("-inf"):
                raise DebugError("`-inf` is not supported")
                # return "-inf"
            elif self.value != self.value:
                raise DebugError("`nan` is not supported")
                # return "nan"
            else:
                return f"{self.value:.7f}"[:-1]
        elif isinstance(self.type, StringType) or (
            isinstance(self.type, OptionType)
            and isinstance(self.type.value_type, StringType)
        ):
            return json.dumps(self.value)
        elif isinstance(self.type, ListType):
            return f"[{', '.join([x.get_value_str() for x in self.value])}]"
        elif isinstance(self.type, UListType):
            return f"u[{', '.join([x.get_value_str() for x in self.value])}]"
        elif isinstance(self.type, IdictType) or isinstance(self.type, SdictType):
            return f"{{{', '.join([f'{k.get_value_str()} => {str(v.get_value_str())}' for k, v in self.value])}}}"
        else:
            raise DebugError(f"Unknown type {self.type}")

    def __str__(self):
        return f"{self.get_value_str()}: {self.type}"

    def from_type_and_node(type: Type, node: ValueNode) -> TypedValue:
        node_pos = (node.start_line, node.start_pos)
        ret = None
        try:
            if isinstance(type, BoolType):
                value = node.value
                if not isinstance(value, str) or not (
                    value == "true" or value == "false"
                ):
                    raise DslValueError(
                        f"Expected `true` or `false` for bool type, but got `{value}`"
                    )
                bool_value = value == "true"
                ret = TypedValue(type, bool_value)
            elif isinstance(type, IntType):
                if not isinstance(node.value, str):
                    raise DslValueError(
                        f"Expected an integer for `int` type, but got `{node.value}`"
                    )
                try:
                    int_value = int(node.value)
                except ValueError:
                    raise DslValueError(
                        f"Expected an integer for `int` type, but got `{node.value}`"
                    )
                if int_value < -2147483648 or int_value > 2147483647:
                    raise DslValueError(
                        f"Expected an integer within [-2147483648, 2147483647] for `int` type, but got `{node.value}`"
                    )
                ret = TypedValue(type, int_value)
            elif isinstance(type, DoubleType):
                if not isinstance(node.value, str):
                    raise DslValueError(
                        f"Expected an numeric value `double` type, but got `{node.value}`"
                    )
                try:
                    double_value = float(node.value)
                except ValueError:
                    raise DslValueError(
                        f"Expected an numeric value type, but got `{node.value}`"
                    )
                ret = TypedValue(type, double_value)
            elif isinstance(type, StringType):
                if not isinstance(node.value, str):
                    raise DslValueError(
                        f"Expected a string for `str` type, but got `{node.value}`"
                    )
                try:
                    str_value = json.loads(node.value)
                except json.JSONDecodeError:
                    raise DslValueError(
                        f"Expected a string in JSON format for `str` type, but got `{node.value}`"
                    )
                for c in str_value:
                    if not c.isprintable() and c not in "\n\t":
                        raise DslValueError(
                            f"Non-printable characters except for `\\n` and `\\t` are not allowed in a string"
                        )
                    elif not c.isascii():
                        raise DslValueError(
                            f"Non-ASCII characters are not allowed in a string"
                        )
                ret = TypedValue(type, str_value)
            elif isinstance(type, ListType):
                list_value = node.value
                if not isinstance(list_value, list):
                    raise DslValueError(
                        f"Expected a list for `list` type, but got `{list_value}`"
                    )
                new_list_value = []
                for value in list_value:
                    new_list_value.append(
                        TypedValue.from_type_and_node(type.value_type, value)
                    )
                ret = TypedValue(type, new_list_value)
                for value in new_list_value:
                    value.parent = ret
            elif isinstance(type, UListType):
                ulist_value = node.value
                if not isinstance(ulist_value, list):
                    raise DslValueError(
                        f"Expected a list for `list` type, but got `{ulist_value}`"
                    )
                new_ulist_value = []
                for value in ulist_value:
                    new_ulist_value.append(
                        TypedValue.from_type_and_node(type.value_type, value)
                    )
                ret = TypedValue(type, new_ulist_value)
                for value in new_ulist_value:
                    value.parent = ret
            elif isinstance(type, IdictType):
                dict_value = node.value
                if not isinstance(dict_value, list) or not all(
                    isinstance(x, tuple) and len(x) == 2 for x in dict_value
                ):
                    raise DslValueError(
                        f"Expected a list of tuples for `dict` type, but got `{dict_value}`"
                    )
                keys = [key for key, value in dict_value]
                if len(keys) != len(set(keys)):
                    raise DslValueError(
                        f"Expected unique keys for `dict` type, but got `{dict_value}`"
                    )
                new_dict_value = []
                for key_value, value_value in dict_value:
                    new_dict_value.append(
                        (
                            TypedValue.from_type_and_node(IntType(), key_value),
                            TypedValue.from_type_and_node(type.value_type, value_value),
                        )
                    )
                ret = TypedValue(type, new_dict_value)
                for key, value in new_dict_value:
                    key.parent = ret
                    value.parent = ret
            elif isinstance(type, SdictType):
                dict_value = node.value
                if not isinstance(dict_value, list) or not all(
                    isinstance(x, tuple) and len(x) == 2 for x in dict_value
                ):
                    raise DslValueError(
                        f"Expected a list of tuples for `dict` type, but got `{dict_value}`"
                    )
                keys = [key for key, value in dict_value]
                if len(keys) != len(set(keys)):
                    raise DslValueError(
                        f"Expected unique keys for `dict` type, but got `{dict_value}`"
                    )
                new_dict_value = []
                for key_value, value_value in dict_value:
                    new_dict_value.append(
                        (
                            TypedValue.from_type_and_node(StringType(), key_value),
                            TypedValue.from_type_and_node(type.value_type, value_value),
                        )
                    )
                ret = TypedValue(type, new_dict_value)
                for key, value in new_dict_value:
                    key.parent = ret
                    value.parent = ret
            elif isinstance(type, OptionType):
                if node.value is None:
                    ret = TypedValue(type, None)
                else:
                    ret = TypedValue.from_type_and_node(type.value_type, node)
                    ret.type = type
            else:
                raise DslValueError(f"Unknown type {type}")
        except DslValueError as e:
            raise DslParseError(node_pos, e)
        return ret
