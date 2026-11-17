#!/bin/bash
set -e

if [ "{{ param_ansible_distribution_major_version }}" -ge 10 ];then
  sudo dnf install -y kernel-modules-extra
fi