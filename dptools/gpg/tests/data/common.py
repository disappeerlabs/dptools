"""
common.py

Common test data for setup and coordination

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import os
from dptools.gpg.tests.data import keys, altkeys


current_key_fingerprint_keys_dir_ring = '1AF427FA3F164D900D7B9913191E11551232B305'


class BaseTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_dir_path = os.path.dirname(keys.__file__)
        cls.alt_key_dir_path = os.path.dirname(altkeys.__file__)
