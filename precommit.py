#!/usr/bin/python
# -*- coding: utf-8 -*-

from subprocess import check_call
import hookutils
import os

if __name__ == '__main__':

    if not hookutils.has_head_ref():
        print 'skipping hooks on initial commit'
        exit(0)

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
