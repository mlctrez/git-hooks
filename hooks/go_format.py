#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import hookutils


def format(files=None, from_git=True):
    """
    Executes go fmt on the provided files.
    """

    for file_in in files:

        file_in = os.path.abspath(file_in)

        before_hash = hookutils.hashfile(file_in)

        hookutils.execute('gofmt -w %s' % file_in)

        if from_git and hookutils.hashfile(file_in) != before_hash:
            print 'gofmt changed %s' % file_in
            hookutils.execute('git add %s' % file_in)


def run():
    os.chdir(hookutils.git_toplevel())

    go_files = filter(lambda x: x.endswith('.go'), hookutils.find_commits())

    format(go_files, from_git=True)


if __name__ == '__main__':
    run()
