# !/usr/bin/env python
import io
import os
from pathlib import Path

from script.domain import default_common as common
from script.utility import template


tmp_api_extra_config=""

def build_extra_config():
    with io.open(common.param_api_extra_config_template_name, "r", encoding="utf-8", newline="\n") as extra_config_template:
        tmp_api_extra_config = Path(common.path_default.output_tmp).resolve().joinpath(
            os.path.basename(common.param_api_extra_config_template_name)).as_posix()
        with io.open(tmp_api_extra_config, "w+", encoding="utf-8", newline="\n") as tmp_output:
            tmp_output.write(template.StringTemplate(extra_config_template.read() + "\n")
                             .safe_substitute(common.getParams()))


def build_override_yml():
    print(build_override_yml.__name__)


def build_api():
    print(build_api.__name__)
