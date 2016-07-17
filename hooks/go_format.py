#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import sys

import hookutils


def format_files(files=None, from_git=True):
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

    from_git = len(sys.argv) == 1

    format_files(hookutils.get_files_to_format('.go'), from_git=from_git)


if __name__ == '__main__':
    run()
