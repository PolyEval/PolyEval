from __future__ import annotations

from polyeval.target.utils import Naming, get_naming_function
from polyeval.target.base.naming import BaseTargetNaming


class LuaTargetNaming(BaseTargetNaming):
    def __init__(self):
        self.func_naming = Naming.SNAKE_CASE
        self.var_naming = Naming.SNAKE_CASE
        pass
