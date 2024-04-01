class DebugError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DslValueError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DslParseError(Exception):
    def __init__(self, pos: tuple[int, int], message: str):
        self.pos = pos
        self.message = message
        super().__init__(f"{message} at (line:{pos[0]}, col:{pos[1]})")


def add_indent(text: str, indent: int) -> str:
    lines = text.split("\n")
    new_lines = ["    " * indent + line for line in lines]
    return ("\n".join(new_lines)).strip()


def is_unrecommended_function_name(name: str) -> bool:
    # "p_e_" is reserved for polyeval internal use
    if name.startswith("p_e_"):
        return True
    names = set()
    # if name is built-in function name or keywords, return false
    return name in names
