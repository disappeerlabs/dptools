"""
basetestclass.py	

> ENTER DESCRIPTION HERE

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""
import os
import unittest

from dptools.gpg.tests.data import keys, altkeys


class BaseTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_dir_path = os.path.dirname(keys.__file__)
        cls.alt_key_dir_path = os.path.dirname(altkeys.__file__)