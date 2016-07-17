#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile

import hookutils


def format_files(files=None, from_git=True):
    """
    Executes tidy on the provided list of files, optionally calling
    git add for each file that changed due to formatting.
    """

    for file_in in files:

        file_in = os.path.abspath(file_in)

        print 'checking %s' % file_in

        if not os.path.exists(file_in):
            print 'missing file %s' % file_in

            continue

        file_out = tempfile.mktemp()
        try:

            import PythonTidy

            reload(PythonTidy)

            # monkeypach constants
            # TODO: make this more configurable

            PythonTidy.COL_LIMIT = 120
            PythonTidy.MAX_SEPS_FUNC_DEF = 8
            PythonTidy.MAX_SEPS_FUNC_REF = 8

            PythonTidy.tidy_up(file_in=file_in, file_out=file_out)

            # overwrite original file only if hash differs

            if hookutils.hashfile(file_in) != hookutils.hashfile(file_out):
                print ' tidying %s' % file_in
                shutil.copymode(file_in, file_out)
                shutil.copy(file_out, file_in)

                # re-add modified file to git if required

                if from_git:
                    hookutils.execute('git add %s' % file_in)
        finally:
            os.remove(file_out)


def run():

    from_git = len(sys.argv) == 1

    format_files(hookutils.get_files_to_format('.py'), from_git=from_git)


if __name__ == '__main__':
    run()
