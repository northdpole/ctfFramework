
from unittest import TestCase

import sys


class BaseTest(TestCase):

    def setUp(self):
        print "BaseTest inited"
        sys.path.append("..")
