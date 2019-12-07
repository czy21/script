# !/usr/bin/env python
import io
import math
import os
import re
import sys
from pathlib import Path

from script.domain import default_common as common
from script.domain.db_meta import mysql as mysql_meta
from script.utility import path, template

commonVars = {k: v for k, v in vars(common).items()
              if isinstance(v, str) and k.startswith("param")}


def build_extra_config():
    with io.open(common.param_api_extra_config_template_name, "r", encoding="utf-8", newline="\n") as extra_config_template:
        tmp_api_extra_config = str(
            Path(common.path_default.output_tmp).resolve().joinpath(os.path.basename(common.param_api_extra_config_template_name)))
        with io.open(tmp_api_extra_config, "w+", encoding="utf-8", newline="\n") as tmp_output:
            tmp_output.write(template.StringTemplate(extra_config_template.read() + "\n")
                             .safe_substitute(commonVars))
