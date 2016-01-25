"""Class to deal with the requested command

.. module:: cmd
    :platform: unix
    :synopsis: it processes the command and takes action based on that

.. moduleauthor:: Minhaz A V <minhazav@gmail.com>
"""

import os
import sys
import time
import json
import sandbox.containerEngine.vagrant.data
import subprocess
import shutil
import re
import random
import string
import threading
from threading import Thread
from sandbox.containerEngine.vagrant.data import vagrantData


class FlagFileNotFound (Exception):
    pass


class helper:
    """helper class to bundle certain required methods"""

    @staticmethod
    def copy(src, dest):
        """Global function to copy file or directory.

        Copies files or directory from source to destination.

        Args:
            src (str): source path of file or dir
            dest (str): destination path of file or dir
        """
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)

    @staticmethod
    def getRootFolder(path):
        """Global function to get root of a relative path

        >>getRootFolder("./dir1/dir2/file")
        dir1

        >>getRootFolder("/dir1")
        dir1

        Args:
            path (str): relative path of a file or dir

        Returns:
            str. The root path of given relative path
        """
        arr = path.split('/')
        if arr[0] == '':
            try:
                return arr[1]
            except:
                return ''
        return arr[0]

    @staticmethod
    def getRandStr(len):
        """Function to get a random string of required length

        Args:
            len (str): the length of random string required

        Returns:
            str. The random string
        """
        return ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(len))

    @staticmethod
    def randomizeFlaginFile(path):
        """Global function to randomize a flag in a file

        The function will read the file and change its value, by
        a random string of same length random string contain uppercase
        alphabets, lowercase alphabets
        AND digits

        Args:
            path (str): the absolute path of the flag
        """
        if not os.path.exists(path):
            raise FlagFileNotFound(
                'no file was found at path given for flag file')

        _flag = ''
        with open(path, 'r+') as _file:
            flag = _file.readline()
            _len = len(flag)
            _flag = helper.getRandStr(_len)

            _file.seek(0)
            _file.write(_flag)
            _file.truncate()
        return _flag

