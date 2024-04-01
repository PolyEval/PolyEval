from __future__ import annotations
import pyparsing as pyp
from polyeval.dsl.node import (
    Node,
    TypeNode,
    VTypeNode,
    KVTypeNode,
    ValueNode,
    QuestionNode,
    FunctionNode,
    ParameterNode,
    TestcaseNode,
    OutFunctionNode,
    OutTestcaseNode,
)

dsl_type = None
dsl_value = None
dsl = None
dsl_output = None


def get_dsl_type():
    global dsl_type
    if dsl_type is not None:
        return dsl_type

    dsl_type = pyp.Forward()
    subtype_start = pyp.Suppress("<")
    subtype_end = pyp.Suppress(">")
    delim = pyp.Suppress(",")

    bool_type = pyp.Suppress("bool")
    int_type = pyp.Suppress("int")
    double_type = pyp.Suppress("double")
    string_type = pyp.Suppress("str")

    bool_type.set_parse_action(
        lambda s, loc, t: TypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "bool")
    )
    int_type.set_parse_action(
        lambda s, loc, t: TypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "int")
    )
    double_type.set_parse_action(
        lambda s, loc, t: TypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "double")
    )
    string_type.set_parse_action(
        lambda s, loc, t: TypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "str")
    )

    list_type = pyp.Suppress("list") + subtype_start + dsl_type + subtype_end
    ulist_type = pyp.Suppress("ulist") + subtype_start + dsl_type + subtype_end

    list_type.set_parse_action(
        lambda s, loc, t: VTypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "list", t[0])
    )
    ulist_type.set_parse_action(
        lambda s, loc, t: VTypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "ulist", t[0])
    )

    dict_type = (
        pyp.Suppress("dict") + subtype_start + dsl_type + delim + dsl_type + subtype_end
    )
    dict_type.set_parse_action(
        lambda s, loc, t: KVTypeNode(
            pyp.lineno(loc, s), pyp.col(loc, s), "dict", t[0], t[1]
        )
    )

    non_option_type = (
        bool_type
        | int_type
        | double_type
        | string_type
        | list_type
        | ulist_type
        | dict_type
    )
    option_type = pyp.Suppress("option") + subtype_start + non_option_type + subtype_end
    option_type_sugar = non_option_type + pyp.Suppress("?")
    option_type = option_type_sugar | option_type
    option_type.set_parse_action(
        lambda s, loc, t: VTypeNode(pyp.lineno(loc, s), pyp.col(loc, s), "option", t[0])
    )

    dsl_type << (option_type | non_option_type)
    return dsl_type


def get_dsl_value():
    global dsl_value
    if dsl_value is not None:
        return dsl_value
    dsl_value = pyp.Forward()

    list_start = pyp.Suppress("[")
    list_end = pyp.Suppress("]")
    dict_start = pyp.Suppress("{")
    dict_end = pyp.Suppress("}")
    delim = pyp.Suppress(",")

    null_literal = pyp.Suppress("null")
    bool_literal = pyp.Literal("true") | pyp.Literal("false")
    int_literal = pyp.Combine(pyp.Optional("-") + pyp.Word(pyp.nums)) + ~pyp.FollowedBy(
        "."
    )
    # double_literal = pyp.Combine(pyp.Optional("-") + pyp.Word(pyp.nums) + "." + pyp.Word(pyp.nums)) | pyp.Literal("nan") | pyp.Combine(pyp.Optional("-") + pyp.Literal("inf"))
    double_literal = pyp.Combine(
        pyp.Optional("-") + pyp.Word(pyp.nums) + "." + pyp.Word(pyp.nums)
    )
    string_literal = pyp.QuotedString(
        quoteChar='"',
        escChar="\\",
        unquoteResults=False,
        multiline=True,
        convertWhitespaceEscapes=False,
    )

    null_literal.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), None)
    )
    bool_literal.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0])
    )
    int_literal.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0])
    )
    double_literal.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0])
    )
    string_literal.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0])
    )

    list_value = list_start + pyp.Optional(pyp.delimitedList(dsl_value)) + list_end
    kv_pair = dsl_value + pyp.Suppress("=>") + dsl_value
    dict_value = dict_start + pyp.Optional(pyp.delimitedList(kv_pair)) + dict_end

    kv_pair.set_parse_action(lambda t: (t[0], t[1]))

    list_value.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), t.as_list())
    )
    dict_value.set_parse_action(
        lambda s, loc, t: ValueNode(pyp.lineno(loc, s), pyp.col(loc, s), t.as_list())
    )

    dsl_value << (
        null_literal
        | bool_literal
        | int_literal
        | double_literal
        | string_literal
        | list_value
        | dict_value
    )
    return dsl_value


def parse_dsl():
    global dsl
    if dsl is not None:
        return dsl
    dsl_type = get_dsl_type()
    dsl_value = get_dsl_value()

    name = pyp.Word(pyp.alphanums + "_")

    def_keyword = pyp.Suppress("def")
    fun_keyword = pyp.Suppress("fun")
    params_start = pyp.Suppress("(")
    params_end = pyp.Suppress(")")
    return_arrow = pyp.Suppress("->")

    parameter_literal = name + pyp.Suppress(":") + dsl_type
    testcase_literal = (
        params_start
        + pyp.Group(pyp.Optional(pyp.delimitedList(dsl_value)))
        + params_end
        + return_arrow
        + dsl_value
    )
    function_literal = (
        fun_keyword
        + name
        + params_start
        + pyp.Group(pyp.Optional(pyp.delimitedList(parameter_literal)))
        + params_end
        + return_arrow
        + dsl_type
        + pyp.Group(pyp.ZeroOrMore(testcase_literal))
    )
    question_literal = def_keyword + name + pyp.Group(pyp.ZeroOrMore(function_literal))

    dsl = pyp.Group(pyp.OneOrMore(question_literal))
    parameter_literal.set_parse_action(
        lambda s, loc, t: ParameterNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0], t[1])
    )
    testcase_literal.set_parse_action(
        lambda s, loc, t: TestcaseNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0], t[1])
    )
    function_literal.set_parse_action(
        lambda s, loc, t: FunctionNode(
            pyp.lineno(loc, s), pyp.col(loc, s), t[0], t[1], t[2], t[3]
        )
    )
    question_literal.set_parse_action(
        lambda s, loc, t: QuestionNode(pyp.lineno(loc, s), pyp.col(loc, s), t[0], t[1])
    )
    dsl.set_parse_action(lambda s, loc, t: list(t))
    return dsl


def parse_dsl_output():
    global dsl_output
    if dsl_output is not None:
        return dsl_output
    dsl_type = get_dsl_type()
    dsl_value = get_dsl_value()

    name = pyp.Word(pyp.alphanums + "_")

    fun_keyword = pyp.Suppress("fun")
    params_start = pyp.Suppress("(")
    params_end = pyp.Suppress(")")
    return_arrow = pyp.Suppress("->")

    function_signature_literal = (
        fun_keyword
        + name
        + params_start
        + pyp.Group(pyp.Optional(pyp.delimitedList(dsl_type)))
        + params_end
        + return_arrow
        + dsl_type
    )

    input_word = pyp.Suppress("input:")
    output_word = pyp.Suppress("output:")
    expected_word = pyp.Suppress("expected:")
    side_effect_word = pyp.Suppress("side-effect:")

    in_literal = (
        input_word
        + params_start
        + pyp.Group(pyp.Optional(pyp.delimitedList(dsl_value)))
        + params_end
    )
    se_literal = (
        side_effect_word
        + params_start
        + pyp.Group(pyp.Optional(pyp.delimitedList(dsl_value)))
        + params_end
    )
    out_literal = output_word + dsl_value
    exp_literal = expected_word + dsl_value

    testcase_start = pyp.Suppress("-")
    testcase_literal = (
        testcase_start + in_literal + out_literal + exp_literal + se_literal
    )
    testcase_literal.set_parse_action(
        lambda s, loc, t: OutTestcaseNode(
            pyp.lineno(loc, s), pyp.col(loc, s), t[0], t[1], t[2], t[3]
        )
    )

    function_literal = function_signature_literal + pyp.Group(
        pyp.ZeroOrMore(testcase_literal)
    )
    function_literal.set_parse_action(
        lambda s, loc, t: OutFunctionNode(
            pyp.lineno(loc, s), pyp.col(loc, s), t[0], t[1], t[2], t[3]
        )
    )

    dsl_output = pyp.Group(pyp.OneOrMore(function_literal))

    return dsl_output


def parse(s: str) -> list[Node]:
    return parse_dsl().parseString(s, parseAll=True)[0]


def parse_output(s: str) -> list[Node]:
    return parse_dsl_output().parseString(s, parseAll=True)[0]
