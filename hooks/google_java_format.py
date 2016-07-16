#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from subprocess import Popen

from hookutils import git_toplevel, hashfile, execute, find_commits

header_cache = None


def get_header():
    global header_cache
    if header_cache is not None:
        return header_cache

    header_file_loc = os.path.join(git_toplevel(), 'JAVA_HEADER')
    if os.path.exists(header_file_loc):
        with open(header_file_loc, 'r') as f:
            copyheader = f.read()
            if copyheader[-1] != '\n':
                copyheader += '\n'
            header_cache = copyheader
    else:
        header_cache = ''
    return header_cache


def add_header(filepath):
    header = get_header()

    if len(header) == 0:

        # don't touch file if no header present

        return

    file_contents = header

    with open(filepath, 'r') as f:
        packageseen = False
        for l in f.readlines():
            if l.startswith('package '):
                packageseen = True

            if packageseen:
                file_contents += l

    if packageseen:
        with open(filepath, 'w') as f:
            f.write(file_contents)


def jar_location():
    return os.path.join(os.environ.get('GIT_HOOKS_HOME'), 'java', 'google-java-format.jar')


def format(files=None, from_git=True):
    """
    Formats java files using the google-java-format jar.
    """

    for file_in in files:

        file_in = os.path.abspath(file_in)

        print 'checking %s' % file_in

        if not os.path.exists(file_in):
            print 'missing file %s' % file_in
            continue

        file_out = tempfile.mktemp()

        command = 'java -jar ' + jar_location() + ' ' + file_in

        try:
            with open(file_out, 'w') as f:
                proc = Popen(command, shell=True, stdout=f)
                proc.wait()
                if proc.returncode != 0:
                    exit(proc.returncode)

            add_header(file_out)

            # overwrite original file only if hash differs

            if hashfile(file_in) != hashfile(file_out):
                print ' formatting %s' % file_in
                shutil.copymode(file_in, file_out)
                shutil.copy(file_out, file_in)

                # re-add to git if file changed

                if from_git:
                    execute('git add %s' % file_in)
        finally:
            os.remove(file_out)


def run():

    os.chdir(git_toplevel())

    java_files = filter(lambda x: x.endswith('.java'), find_commits())

    format(java_files, from_git=True)


if __name__ == '__main__':
    run()
