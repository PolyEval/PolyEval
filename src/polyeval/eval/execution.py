from __future__ import annotations

import os
import random

import yaml
import subprocess
from yaml import CLoader
from pathlib import Path
import shutil

from polyeval.misc.utils import add_indent


class ExecutionTarget:
    def __init__(
        self,
        name: str,
        cwd: os.PathLike,
        main: os.PathLike,
        run: str,
        symlink: list[os.PathLike],
    ):
        self.name = name
        if not os.path.exists(cwd):
            raise FileNotFoundError(f"Directory `{cwd}` not found")
        self.cwd = cwd
        if not os.path.exists(main):
            raise FileNotFoundError(f"Main file `{main}` not found")
        elif not Path(main).is_relative_to(cwd):
            raise ValueError(f"Main file `{main}` must be relative to cwd `{cwd}`")
        self.main = main
        with open(main, "r", encoding="utf-8") as f:
            self.code = f.read()
            assert (
                self.code.count("$$code$$") == 1
            ), f"File `{main}` should contain exactly one `$$code$$`"
        self.run = run
        self.symlink = symlink
        for link in symlink:
            if not os.path.exists(link):
                raise FileNotFoundError(f"Symlink file `{link}` not found")
            elif not Path(link).is_relative_to(cwd):
                raise ValueError(
                    f"Symlink file `{link}` must be relative to cwd `{cwd}`"
                )


class ExecutionProject:
    def __init__(self, cwd: os.PathLike, run: str):
        self.cwd = cwd
        self.run = run

    def execute(self, timeout=20) -> (bool, str):
        result = subprocess.run(
            self.run,
            cwd=self.cwd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
        if result.returncode != 0:
            return False, None
        output_path = os.path.join(self.cwd, "result.out")
        if not os.path.exists(output_path):
            return False, None
        with open(os.path.join(self.cwd, "result.out"), "r", encoding="utf-8") as f:
            result = f.read()
        return True, result

    def clean(self):
        if os.path.exists(self.cwd):
            shutil.rmtree(self.cwd)


class ExecutionTemplate:
    def __init__(self, dir: str, targets: dict[str, ExecutionTarget]):
        self.dir = dir
        self.targets = targets

    def create_execution_project(
        self,
        target_name: str,
        code: str,
        proj_name: str = None,
        exist_ok=False,
        root_dir: os.PathLike = "./.polyeval",
    ) -> ExecutionProject:
        if target_name not in self.targets:
            raise ValueError(f"Target {target_name} not found in template")

        if proj_name == None:
            proj_dir = None
            while proj_dir is None or os.path.exists(proj_dir):
                random_name = "".join(
                    random.choice("0123456789ABCDEF") for i in range(16)
                )
                proj_dir = os.path.join(root_dir, random_name)
        else:
            proj_dir = os.path.join(root_dir, proj_name)
            if os.path.exists(proj_dir):
                if not exist_ok:
                    raise FileExistsError(f"Directory `{proj_dir}` already exists")
                else:
                    shutil.rmtree(proj_dir)

        os.makedirs(proj_dir)

        template = self.targets[target_name]
        template_cwd = template.cwd
        template_code = template.code
        indent_spaces = template_code.split("$$code$$")[0].split("\n")[-1]
        assert len(indent_spaces) % 4 == 0
        indents = len(indent_spaces) // 4

        insert_code = add_indent(code, indents)
        final_code = template_code.replace("$$code$$", insert_code)

        proj_main_path = os.path.join(
            proj_dir, os.path.relpath(template.main, template_cwd)
        )
        os.makedirs(os.path.dirname(proj_main_path), exist_ok=True)

        with open(proj_main_path, "w") as f:
            f.write(final_code)

        for link in template.symlink:
            target_path = os.path.join(proj_dir, os.path.relpath(link, template_cwd))
            os.symlink(os.path.abspath(link), target_path)
            # print("Symlink", os.path.abspath(link), "to", target_path)

        return ExecutionProject(proj_dir, template.run)


def initialize_template(
    dir: os.PathLike, config_path: os.PathLike = None, targets: list[str] = None
) -> ExecutionTemplate:
    if not os.path.exists(dir):
        raise FileNotFoundError(f"Directory `{dir}` not found")
    if config_path is None:
        config_path = os.path.join(dir, "polyeval.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file `{config_path}` not found")
    # open yaml file to python dict
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=CLoader)

    config_targets = config["targets"]

    avaliable_target_names = list(config_targets.keys())
    if targets is None:
        targets_names = avaliable_target_names
    else:
        targets_names = targets

    target_dicts = {}
    for name in targets_names:
        if name not in avaliable_target_names:
            raise ValueError(f"Target {target_name} not found in config file")

        target = config_targets[name]
        if "cwd" not in target or "main" not in target or "run" not in target:
            raise ValueError(f"Invalid configuration for target {name}")

        cwd = os.path.join(dir, target["cwd"])
        if os.path.isabs(cwd):
            raise ValueError(f"Cwd directory `{cwd}` must be an relative path")

        main = os.path.join(cwd, target["main"])
        if os.path.isabs(main):
            raise ValueError(f"Main file `{main}` must be an relative path")

        symlink = []
        if "symlink" in target:
            assert isinstance(
                target["symlink"], list
            ), "`symlink` of target must be a list"
            for link in target["symlink"]:
                if os.path.isabs(link):
                    raise ValueError(f"Symlink file `{link}` must be an relative path")
                symlink.append(os.path.join(cwd, link))

        target_dicts[name] = {
            "cwd": cwd,
            "main": main,
            "run": target["run"],
            "symlink": symlink,
        }

    # prepare the template
    for name in targets_names:
        target = config_targets[name]
        target_dict = target_dicts[name]
        if "prepare" in target:
            prepare_cmd = target["prepare"]
            result = subprocess.run(
                prepare_cmd,
                cwd=target_dict["cwd"],
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            assert (
                result.returncode == 0
            ), f"Prepare command execution failed for target `{name}`"
            print("Prepare Ready for target", name)

    target_objects = {}
    for name, target_dict in target_dicts.items():
        target_objects[name] = ExecutionTarget(name, **target_dict)

    return ExecutionTemplate(dir, target_objects)
