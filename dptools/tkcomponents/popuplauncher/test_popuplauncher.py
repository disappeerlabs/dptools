"""
test_popuplauncher.py	

Tests for the popuplauncher integration module.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from dptools.tkcomponents.popuplauncher import launch_popup, alertbox


class TestPopupLauncher(unittest.TestCase):

    def setUp(self):
        self.mock_root = MagicMock()
        self.message = 'vrw3ew32'
        self.output = 'ewqfewvrb'
        self.sub1 = alertbox.alertboxcontroller.AlertBoxController = MagicMock()
        self.sub2 = alertbox.alertboxcontroller.AlertBoxController(self.mock_root, self.message).show = MagicMock(return_value=self.output)

    def test_launch_popup_calls_target_controller(self):
        o = launch_popup(alertbox, self.mock_root, self.message)
        self.assertTrue(self.sub1.called)
        self.sub1.assert_called_with(self.mock_root, self.message)

    def test_launch_popup_calls_show_and_returns_output(self):
        o = launch_popup(alertbox, self.mock_root, self.message)
        self.assertTrue(self.sub2.called)
        self.assertEqual(o, self.output)
