from __future__ import annotations

from polyeval.target.utils import Naming, get_naming_function


class BaseTargetNaming:
    def __init__(self):
        self.func_naming = Naming.SNAKE_CASE
        self.var_naming = Naming.SNAKE_CASE
        pass

    def get_func_name(self, name):
        return get_naming_function(self.func_naming)(name)

    def get_var_name(self, name):
        return get_naming_function(self.var_naming)(name)
