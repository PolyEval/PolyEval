from __future__ import annotations

from polyeval.target.utils import Naming, get_naming_function
from polyeval.target.base.naming import BaseTargetNaming


class NimTargetNaming(BaseTargetNaming):
    def __init__(self):
        self.func_naming = Naming.CAMEL_CASE
        self.var_naming = Naming.CAMEL_CASE
        pass
