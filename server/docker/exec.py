#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-i', action="store_true")
parser.add_argument('-c', action="store_true")
args = parser.parse_args()

list_dir = [p for p in Path(__file__).parent.iterdir() if p.is_dir()]

print("\n==========")

for i, p in enumerate(list_dir, start=1):
    print(" ".join([str(i), p.name]))

one_option = input("please select one option(example:1) ").strip()
if not one_option.isnumeric():
    print("\ninvalid option")
    sys.exit()

one_option = int(int(one_option))

if not one_option in [i for i, p in enumerate(list_dir, start=1)]:
    print(" ".join(["\n", one_option, "not exist"]))
    sys.exit()

app_paths = enumerate([p for p in Path(__file__).parent.joinpath(list_dir[one_option]).iterdir() if p.is_dir()], start=1)

for i, p in app_paths:
    print(" ".join([str(i), p.name]))

app_options = input("please select app number(example:1 2 3) ").strip().split()

print("fff")
# install_tuple = [int(t) for t in app_options if t.isnumeric() and t in [str(i) for i in app_paths]]

print([i for i,p in enumerate(app_paths, start=1)])
# print(app_paths)1
# print(app_options)
# print(install_tuple)
