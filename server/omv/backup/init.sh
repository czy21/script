#!/bin/bash

mkdir -p $HOME/backup/target
cp -rv {{ param_role_output_path }}/target/ $HOME/backup/