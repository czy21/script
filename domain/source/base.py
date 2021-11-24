#!/usr/bin/env python3
import inspect
import io
from pathlib import Path

from script.utility.template import CustomTemplate

from script.domain.default import common as default_common
from script.utility import basic as basic_util, collection as list_util, log
logger = log.Logger(__name__)


def __get_function_name():
    return inspect.stack()[1][3]


def build_by_template(template_name, output_path):
    Path(output_path).parent.mkdir(exist_ok=True, parents=True)
    content = CustomTemplate(filename=template_name).render(**dict({k: v for k, v in default_common.__dict__.items() if k.startswith("param")}))
    with io.open(output_path, "w+", encoding="utf-8", newline="\n") as target_output:
        target_output.write(content)
