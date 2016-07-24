#!/usr/bin/python
# -*- coding: utf-8 -*-

import errno
import hashlib
import os
import sys
from subprocess import Popen, PIPE, CalledProcessError, check_output


# GIT_DIFF_INDEX =
# GIT_DIFF_NO_HEAD = 'git diff-index --diff-filter=ACM --cached --name-only 4b825dc642cb6eb9a060e54bf8d69288fbee4904'

def execute(command, fail_on_error=True):
    """
    Execute a command and returns the standard output lines.
    If the command exits with a non-zero exit code and fail_on_error is true
    then this script exits with a non zero exit code, which signals git-commit to fail.

    :param command: the command to execute
    :param fail_on_error: true if the script should exit on a non zero command exit
    """

    lines = []
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    for line in proc.stdout.readlines():
        lines.append(line.strip())
    for line in proc.stderr.readlines():
        if line[:len('exit status')] != 'exit status':
            print 'stderr> %s' % line.strip()
    proc.wait()
    code = proc.returncode
    if code != 0 and fail_on_error:
        print 'exit code = %s' % code
        exit(code)
    return lines


def calculate_head():
    try:
        return check_output('git rev-parse --verify HEAD', shell=True, stderr=PIPE).strip()
    except CalledProcessError:
        return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'


def mkdir_p(path):
    """
    Create subdirectories without throwing an error if the directories exist
    Origin http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """

    try:
        os.makedirs(path)
    except OSError, exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):

            pass
        else:
            raise


def find_commits():
    return execute('git diff-index --diff-filter=ACM --cached --name-only ' + os.environ['_GIT_HEAD'])


def hashfile(file_path):
    """
    Calculates the hash of a provided file path.
    :param file_path: file to calculate the hash
    """

    blocksize = 8192
    afile = open(file_path, 'r')
    buf = afile.read(blocksize)
    hasher = hashlib.md5()
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()

    return hasher.hexdigest()


def in_git_directory():
    try:
        git_toplevel()
        return True
    except CalledProcessError:
        return False


def git_toplevel():
    """
    Returns the git toplevel directory
    """

    return check_output('git rev-parse --show-toplevel', shell=True, stderr=PIPE).strip()


def get_files_to_format(extension):

    def extension_filter(filename):
        return filename.endswith(extension)

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        return filter(extension_filter, args)
    else:
        os.chdir(git_toplevel())
        return filter(extension_filter, find_commits())


