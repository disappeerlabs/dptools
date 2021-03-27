"""
test_basemodel.py
"""

import unittest
from unittest.mock import MagicMock
from dptools.tkcomponents.baseapp import basemodel


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.mock_args = MagicMock()
        self.mock_root = MagicMock()
        self.x = basemodel.BaseModel(args=self.mock_args, root=self.mock_root)
    
    def test_kwargs_set(self):
        self.assertEqual(self.x.root, self.mock_root)
        self.assertEqual(self.x.args, self.mock_args)
    
    def test_register_widget_model(self):
        name = 'hello_there'
        val = MagicMock
        res = self.x.register_widget_model(name, val)
        o = getattr(self.x, name)
        self.assertIsInstance(o, val)


