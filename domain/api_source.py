# !/usr/bin/env python
import io
import os
from pathlib import Path

from colorama import Fore, init

from script.domain.default import default_common as common
from script.utility import template

init(autoreset=True)


def build_by_template(template_name, output_path):
    output_name = Path(output_path).resolve().joinpath(os.path.basename(template_name)).as_posix()
    with io.open(template_name, "r", encoding="utf-8", newline="\n") as source_template:
        with io.open(output_name, "w+", encoding="utf-8", newline="\n") as target_output:
            target_output.write(template.StringTemplate(source_template.read() + "\n")
                                .safe_substitute(common.get_params()))
    return output_name


def build_extra_config():
    print(Fore.CYAN + build_extra_config.__name__)
    return build_by_template(common.param_api_extra_config_template_name, common.path_default.output_tmp)


def build_override_yml():
    print(Fore.CYAN + build_override_yml.__name__)
    return build_by_template(common.param_api_yml_override_template_name, common.param_api_output_resource_path)


def build_api():
    output_extra_config_name = build_extra_config()
    command = "gradle clean build" \
              " --build-file " + Path(common.param_api_root_project_path).joinpath("build.gradle").as_posix() + \
              " --project-prop extraConfig=" + output_extra_config_name
    print(Fore.CYAN + build_api.__name__ + " => " + Fore.WHITE + command)
    os.system(command)
    build_override_yml()
