#!/usr/bin/env python3
import io

from script.domain.default import common as default_common
from script.utility.template import CustomTemplate


def build_by_template(template_name, output_path):
    content = CustomTemplate(filename=template_name).render(**default_common.get_params())
    with io.open(output_path, "w+", encoding="utf-8", newline="\n") as target_output:
        target_output.write(content)
