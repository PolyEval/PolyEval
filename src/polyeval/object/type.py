from __future__ import annotations
from polyeval.dsl.node import TypeNode, VTypeNode, KVTypeNode
from polyeval.misc.utils import DslValueError, DslParseError, DebugError


class Type:
    def __init__(self):
        self.parent: Type = None

    def __str__(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def from_node(node: TypeNode) -> Type:
        type_name = node.type_name
        node_pos = (node.start_line, node.start_pos)
        ret = None
        try:
            if not isinstance(node, VTypeNode):
                if type_name == "bool":
                    ret = BoolType()
                elif type_name == "int":
                    ret = IntType()
                elif type_name == "double":
                    ret = DoubleType()
                elif type_name == "str":
                    ret = StringType()
                else:
                    raise DslValueError(f"Unknown type {node.type_name}")
            elif isinstance(node, VTypeNode) and not isinstance(node, KVTypeNode):
                value_type = Type.from_node(node.value_type)
                if type_name == "list":
                    ret = ListType(value_type)
                elif type_name == "ulist":
                    ret = UListType(value_type)
                elif type_name == "option":
                    ret = OptionType(value_type)
                else:
                    raise DslValueError(f"Unknown type {node.type_name}")
            elif isinstance(node, KVTypeNode):
                key_type = Type.from_node(node.key_type)
                value_type = Type.from_node(node.value_type)
                if type_name == "dict":
                    if isinstance(key_type, IntType):
                        ret = IdictType(value_type)
                    elif isinstance(key_type, StringType):
                        ret = SdictType(value_type)
                    else:
                        raise DslValueError(f"Dict type must has int or str key")
                else:
                    raise DslValueError(f"Unknown type {node.type_name}")
        except DslValueError as e:
            raise DslParseError(node_pos, e)
        return ret


class VType(Type):
    def __init__(self, value_type: Type):
        super().__init__()
        self.value_type: Type = value_type
        value_type.parent = self


class BoolType(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "bool"


class IntType(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "int"


class DoubleType(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "double"


class StringType(Type):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "str"


class ListType(VType):
    def __init__(self, value_type: Type):
        super().__init__(value_type)
        if not isinstance(value_type, Type):
            raise DebugError("value_type must be of type Type")
        self.value_type: Type = value_type
        value_type.parent = self

    def __str__(self):
        return f"list<{self.value_type}>"


class UListType(VType):
    def __init__(self, value_type: Type):
        super().__init__(value_type)
        if not isinstance(value_type, Type):
            raise DebugError("value_type must be of type Type")
        self.value_type: Type = value_type
        value_type.parent = self

    def __str__(self):
        return f"ulist<{self.value_type}>"


class IdictType(VType):
    def __init__(self, value_type: Type):
        super().__init__(value_type)
        if not isinstance(value_type, Type):
            raise DebugError("value_type must be of type Type")
        elif isinstance(value_type, OptionType):
            raise DslValueError("Can't have option type as value type of dict")
        self.value_type: Type = value_type
        value_type.parent = self

    def __str__(self):
        return f"dict<int,{self.value_type}>"


class SdictType(VType):
    def __init__(self, value_type: Type):
        super().__init__(value_type)
        if not isinstance(value_type, Type):
            raise DebugError("value_type must be of type Type")
        elif isinstance(value_type, OptionType):
            raise DslValueError("Can't have option type as value type of dict")
        self.value_type: Type = value_type
        value_type.parent = self

    def __str__(self):
        return f"dict<str,{self.value_type}>"


class OptionType(VType):
    def __init__(self, value_type: Type):
        super().__init__(value_type)
        if not isinstance(value_type, Type):
            raise DebugError("value_type must be of type Type")
        if isinstance(value_type, VType):
            raise DslValueError("Can only have option of basic types")
        self.value_type: Type = value_type
        value_type.parent = self

    def __str__(self):
        return f"option<{self.value_type}>"
