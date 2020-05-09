"""
test_observable.py

TDD tests for observable class object.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from dptools.utilities import observable


class ObservableTest(unittest.TestCase):

    def setUp(self):
        self.o = observable.Observable()

    def test_exists(self):
        """Observable class object exists"""
        self.assertIsInstance(self.o, observable.Observable)

    def test_data_param(self):
        """Set data param on obj init"""
        msg = 'Hello World'
        o = observable.Observable(msg)
        self.assertEqual(o.data, msg)
        self.assertEqual(o.get(), msg)

    # @unittest.expectedFailure
    # def test_callbacks_param_default_has_callback(self):
    #     """
    #     Set callbacks param on obj.
    #     The update_observers method is added as initial callback
    #     on all observables.
    #     """
    #     self.assertEqual(len(self.o.callbacks), 1)

    def test_callbacks_param_default_is_empty(self):
        """
        Set callbacks param on obj
        """
        self.assertEqual(self.o.callbacks, {})

    def test_get(self):
        """Get should return current data"""
        val = []
        o = observable.Observable(val)
        result = o.get()
        self.assertEqual(result, val)

    def test_set(self):
        """Should update current data"""
        val = []
        o = observable.Observable(val)
        target = True
        o.set(target)
        self.assertEqual(o.data, target)
        self.assertEqual(o.get(), target)

    def test_unset(self):
        """Should update data to none"""
        val = []
        o = observable.Observable(val)
        o.unset()
        self.assertEqual(o.data, None)
        self.assertEqual(o.get(), None)

    def test_set_calls_run_callbacks(self):
        """Should update current data"""
        val = []
        o = observable.Observable(val)
        mock = MagicMock()
        o.add_callback(mock)
        target = 'hello there'
        o.set(target)
        self.assertIs(mock.called, True)

    def test_set_calls_update_observers(self):
        """Setting observable should result in setting observer"""

    def test_add_callback(self):
        """Add callback should update the callback attribute"""
        mock = MagicMock()
        self.o.add_callback(mock)
        self.assertEqual(len(self.o.callbacks), 1)
        self.assertIn(mock, self.o.callbacks)

    def test_run_callbacks_method_runs_callback_funcs(self):
        mock = MagicMock(return_value=True)
        self.o.add_callback(mock)
        self.o.run_callbacks()
        self.assertIs(mock.called, True)

    def test_delete_callback_removes_func_from_callback_list(self):
        mock = MagicMock(return_value=True)
        self.o.add_callback(mock)
        self.assertEqual(len(self.o.callbacks), 1)
        self.o.delete_callback(mock)
        self.assertEqual(len(self.o.callbacks), 0)

    def test_update_widget_attribute(self):
        name = 'update_widget'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_update_widget_calls_set_on_arg(self):
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.set = MagicMock()

        msg = 'XXX^666'
        self.o.set(msg)
        self.o.update_widget(mock)
        mock.set.assert_called_with(msg)

    def test_observer_list_attribute(self):
        name = 'observer_list'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_observer_list_attribute_is_list(self):
        self.assertEqual([], self.o.observer_list)

    def test_add_observer_attribute(self):
        name = 'add_observer'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_add_observer_method_adds(self):
        obs = MagicMock()
        self.o.add_observer(obs)
        self.assertIn(obs, self.o.observer_list)

    def test_add_observer_calls_set_on_observer_not_selfs_set(self):
        obs_mock = MagicMock()
        sub = obs_mock.set = MagicMock()

        val = 'hello then'
        o = observable.Observable(val)
        o.add_observer(obs_mock)
        sub.assert_called_with(val)

    def test_update_observers_attribute(self):
        name = 'update_observers'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_update_observers_calls_observers(self):
        from unittest.mock import MagicMock
        obs = MagicMock()
        obs.set = MagicMock()

        self.o.add_observer(obs)
        self.o.set("HELLO THERE")
        self.assertTrue(obs.set.called)


if __name__ == '__main__':
    unittest.main()
