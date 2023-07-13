#!/bin/bash
python3 -m pip install -r requirements.txt
mkdocs build && tar -zcvf doc.tar.gz -C build doc