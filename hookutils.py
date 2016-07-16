#!/usr/bin/python
# -*- coding: utf-8 -*-

import errno
import hashlib
import os
from subprocess import Popen, PIPE, STDOUT, CalledProcessError, check_output

GIT_DIFF_INDEX = 'git diff-index --name-status --cached HEAD'


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
        print 'stderr> %s' % line.strip()
    proc.wait()
    code = proc.returncode
    if code != 0 and fail_on_error:
        print 'exit code = %s' % code
        exit(code)
    return lines


def has_head_ref():
    """
    Check if this is the first commit, preventing errors in downstream hooks
    that use "git diff-index --name-status --cached HEAD"
    :return: true if .git/HEAD points to a non existent .git/refs/heads file
    """

    try:
        check_output(GIT_DIFF_INDEX, stderr=STDOUT, shell=True)
        return True
    except CalledProcessError:
        return False


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
    changed_files = []
    status_lines = execute(GIT_DIFF_INDEX)
    for line in status_lines:
        line = line.strip()

        # output is FLAG\tFILENAME

        (flag, filename) = line.split('\t')

        # we're not concerned with delete files

        if flag is 'D':
            continue
        changed_files.append(filename)
    return changed_files


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


def git_toplevel():
    """
    Returns the git toplevel directory
    """

    return execute('git rev-parse --show-toplevel')[0]


