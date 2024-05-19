from __future__ import annotations

import os
import random

from polyeval.misc.utils import add_indent
from polyeval.object.question import Question
from polyeval.eval.execution import ExecutionTemplate, ExecutionProject
from polyeval.object.output_result import parse_result

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

def get_test_code(lang: str, question: Question) -> str:
    return find_target(lang).tests_generator.gen_code(question.functions)

def create_evalution_project(
    template: ExecutionTemplate,
    lang: str,
    question: Question,
    code: str,
    proj_name=None,
    exist_ok=False,
) -> ExecutionProject:
    if lang not in template.targets:
        raise ValueError(f"Language `{lang}` not found in execution template")
    test_code = get_test_code(lang, question)
    final_code = code + "\n" + test_code
    if proj_name is not None:
        name = proj_name
    else:
        name = f"{lang}-{question.name}"
    return template.create_execution_project(lang, final_code, name, exist_ok=exist_ok)


def evaluate(
    template: ExecutionTemplate,
    lang: str,
    question: Question,
    code: str,
    proj_name=None,
    exist_ok=False,
    clean=False,
    clean_when_succeed=True,
) -> (bool, str):
    project = create_evalution_project(
        template, lang, question, code, proj_name, exist_ok=exist_ok
    )
    status, result = project.execute()
    if clean:
        project.clean()
    if not status:
        return False, "Execution Failed"
    try:
        funcs = parse_result(result)
    except Exception as e:
        return False, f"Error parsing output: {e}"
    is_expected = True
    for func in funcs:
        if not func.is_expected():
            func.pretty_print()
            is_expected = False
            break
    if not is_expected:
        return False, "Output not expected"
    is_no_side_effect = True
    for func in funcs:
        if not func.is_no_side_effect():
            func.pretty_print()
            is_no_side_effect = False
            break
    if not is_no_side_effect:
        return False, "Side effect detected"
    if clean_when_succeed:
        project.clean()
    return status, "OK"
