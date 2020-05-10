"""
test_constants.py	

Basic tests for dptools constants file

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.static import constants


class TestBasicConstants(unittest.TestCase):

    def test_command_list_named_tuple_objs(self):
        self.assertEqual(type(constants.command_list_inputs), type(list()))
        for item in constants.command_list_inputs:
            self.assertIn(item, dir(constants.command_list_tuple_obj))
            self.assertIn(item, dir(constants.command_list))

    def test_command_list_create_new_key(self):
        txt = "Create_New_Key"
        self.assertEqual(constants.command_list.Create_New_Key, txt)

    def test_command_list_check_sanity(self):
        txt = "Check_Sanity"
        self.assertEqual(constants.command_list.Check_Sanity, txt)
