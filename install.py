#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Installs all of the necessary dependencies for the hooks.
"""

import os
import shutil
import sys
import urllib

from subprocess import check_call
from hookutils import mkdir_p


def install_directory():
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def install_file(src_url, dest_file):
    if not os.path.exists(dest_file):
        urllib.urlretrieve(src_url, dest_file)


def get_pytidy():
    tidy_url = 'http://lacusveris.com/PythonTidy/PythonTidy-1.22.python'

    inst_dir = os.path.join(install_directory(), 'python')
    mkdir_p(inst_dir)

    tidy_file_local = os.path.join(inst_dir, 'PythonTidy.py')

    install_file(tidy_url, tidy_file_local)


def get_google_format_jar():
    jar_url = 'https://github.com/google/google-java-format/releases/download'
    jar_url += '/google-java-format-1.0/google-java-format-1.0-all-deps.jar'

    inst_dir = os.path.join(install_directory(), 'java')
    mkdir_p(inst_dir)

    jar_local = os.path.join(inst_dir, 'google-java-format.jar')

    install_file(jar_url, jar_local)


def install_template():
    gt_dir = os.path.expanduser('~/.git_template')

    if os.path.exists(gt_dir):
        fail_with_message('%s exists, not overwriting' % gt_dir)
    hooks_template_dir = os.path.join(gt_dir, 'hooks')
    mkdir_p(hooks_template_dir)

    src_file = os.path.join(install_directory(), 'pre-commit.template')
    dst_file = os.path.join(hooks_template_dir, 'pre-commit')

    with open(src_file, 'r') as t:
        template_contents = t.read()

    template_contents = template_contents.replace('@@GIT_HOOKS_HOME@@', install_directory())

    with open(dst_file, 'w') as t:
        t.write(template_contents)

    shutil.copystat(src_file, dst_file)

    check_call("git config --global init.templatedir '%s'" % gt_dir, shell=True)


def fail_with_message(message):
    print message
    exit(1)


if __name__ == '__main__':
    get_pytidy()
    get_google_format_jar()
    install_template()
