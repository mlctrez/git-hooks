#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile

import hookutils


def tidy_files(files=None, from_git=True):
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

    os.chdir(hookutils.git_toplevel())

    python_files = filter(lambda x: x.endswith('.py'), hookutils.find_commits())

    tidy_files(python_files, from_git=True)


if __name__ == '__main__':
    run()

