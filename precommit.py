#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import check_call

import hookutils

if __name__ == '__main__':

    os.environ['_GIT_HEAD'] = hookutils.calculate_head()

    home = os.environ.get('GIT_HOOKS_HOME', None)
    if not home:
        print 'unable to determine GIT_HOOKS_HOME environment'
        exit(1)

    hook_dir = os.path.join(home, 'hooks')

    print 'executing hooks in %s' % hook_dir

    for f in os.listdir(hook_dir):
        h = os.path.join(hook_dir, f)
        if os.path.isfile(h):
            check_call('python %s' % h, shell=True)
