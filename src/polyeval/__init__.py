from polyeval.object.question import parse_questions
from polyeval.object.output_result import parse_result
from polyeval.eval.execution import initialize_template
from polyeval.eval.evaluation import evaluate

import importlib

def find_target(lang: str) -> str:
    target_package_name = f"polyeval.target.{lang}"
    try:
        target_package = importlib.import_module(target_package_name)
    except ModuleNotFoundError:
        target_package = None
    if target_package is None:
        extra_target_package_name = f"polyeval_extra.target.{lang}"
        try:
            target_package = importlib.import_module(extra_target_package_name)
        except ModuleNotFoundError:
            raise ValueError(f"No generator for {lang} found")
    return target_package
