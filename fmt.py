#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import check_call


def run():
    hooks_home = os.path.dirname(os.path.realpath(sys.argv[0]))

    # same as pre-commit.template
    os.environ['GIT_HOOKS_HOME'] = hooks_home
    os.environ['PYTHONPATH'] = "%s:%s/python" % (hooks_home, hooks_home)

    hook_dir = os.path.join(hooks_home, 'hooks')

    for f in os.listdir(hook_dir):
        h = os.path.join(hook_dir, f)
        if os.path.isfile(h):
            check_call('python %s' % h, shell=True)

if __name__ == '__main__':
    run()

