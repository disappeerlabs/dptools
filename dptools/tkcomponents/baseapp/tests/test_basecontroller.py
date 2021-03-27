"""
test_basecontroller.py


"""

import unittest
from unittest.mock import MagicMock
from dptools.tkcomponents.baseapp import (
    basecontroller, 
    queueconsumer, 
    basepanelview, 
    basemodel)


class TestBaseController(unittest.TestCase):

    def setUp(self):
        self.mock_args = MagicMock()
        self.mock_root = MagicMock()
        self.x = basecontroller.BaseController(root=self.mock_root, args=self.mock_args)

    def test_kwargs_set(self):
        self.assertEqual(self.x.root, self.mock_root)
        self.assertEqual(self.x.args, self.mock_args)

    def test_is_queueconsumer(self):
        self.assertIsInstance(self.x, queueconsumer.QueueConsumer)
    
    def test_root_view_is_set(self):
        self.assertIsInstance(self.x.root_view, basepanelview.BasePanelView)

    def test_root_model_is_set(self):
        self.assertIsInstance(self.x.root_model, basemodel.BaseModel)

    def test_register_widget(self):
        mock_component = MagicMock()
        target_method = mock_component.register_widget = MagicMock()
        target_return_value = target_method.return_value = 12345
        mock_view_method = MagicMock()
        mock_model_method = MagicMock()
        o = self.x.register_widget(mock_component, mock_view_method, mock_model_method)
        target_method.assert_called_with(self.mock_root, mock_view_method, mock_model_method)
        self.assertEqual(o, target_return_value)
    
    def test_add_widget_left_panel(self):
        mock_component = MagicMock()
        target_method = self.x.register_widget = MagicMock()
        target_val = 123456
        target_method.return_value = target_val
        o = self.x.add_widget_left_panel(mock_component)
        target_method.assert_called_with(mock_component, self.x.root_view.add_tab_to_left_panel, self.x.root_model.register_widget_model)
        self.assertEqual(o, target_method.return_value)

    def test_add_widget_right_panel(self):
        mock_component = MagicMock()
        target_method = self.x.register_widget = MagicMock()
        target_val = 123456
        target_method.return_value = target_val
        o = self.x.add_widget_right_panel(mock_component)
        target_method.assert_called_with(mock_component, self.x.root_view.add_tab_to_right_panel, self.x.root_model.register_widget_model)
        self.assertEqual(o, target_method.return_value)
