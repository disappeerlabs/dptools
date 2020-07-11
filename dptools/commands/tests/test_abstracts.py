"""
test_abstracts.py	

Tests for the abstracts.py module containing ABCs for command pattern implementation

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from dptools.commands import abstracts
from dptools.tkcomponents.baseapp.queueconsumer import QueueConsumer


class ConcreteCommand(abstracts.AbstractCommand):

    def __init__(self, first=None, second=None):
        super().__init__(first=first, second=second)


class TestAbstractCommand(unittest.TestCase):

    def setUp(self):
        self.x = 'x'
        self.y = 'y'
        self.valid_obj = ConcreteCommand(first=self.x, second=self.y)

    def test_metaclass_attribute(self):
        check = hasattr(self.valid_obj, '_abc_impl')
        self.assertTrue(check)

    def test_abstract_command_name_is_classname(self):
        self.assertEqual(ConcreteCommand.__name__, self.valid_obj.name)

    def test_abstract_command_sets_kwargs(self):
        self.assertEqual(self.valid_obj.first, self.x)
        self.assertEqual(self.valid_obj.second, self.y)


class ConcreteHandlerValid(abstracts.AbstractHandler):

    def __init__(self, destination_queue):
        super().__init__(destination_queue)

    def handle(self, arg):
        pass


class ConcreteHandlerNotValidNoHandle(abstracts.AbstractHandler):

    def __init__(self, destination_queue):
        super().__init__(destination_queue)


class TestAbstractHandler(unittest.TestCase):

    def setUp(self):
        self.mock_queue = MagicMock()
        self.x = ConcreteHandlerValid(self.mock_queue)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_impl')
        self.assertTrue(check)

    def test_handler_has_queue_attr_set(self):
        self.assertEqual(self.mock_queue, self.x.destination_queue)

    def test_handler_has_handle_method(self):
        with self.assertRaises(TypeError):
            x = ConcreteHandlerNotValidNoHandle(self.mock_queue)

    def test_abstract_handler_method_takes_arg(self):
        mock_command = MagicMock()
        try:
            self.x.handle(mock_command)
        except:
            self.assertTrue(False, "handle method should take arg")


class ConcreteResult(abstracts.AbstractResult):

    def __init__(self, result):
        super().__init__(result)


class TestAbstractResult(unittest.TestCase):

    def setUp(self):
        self.mock_result = MagicMock()
        self.x = ConcreteResult(self.mock_result)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_impl')
        self.assertTrue(check)

    def test_abstract_result_name(self):
        self.assertEqual(ConcreteResult.__name__, self.x.name)

    def test_abstract_result_result_set(self):
        self.assertEqual(self.x.result, self.mock_result)


class TestCreateCallbackFunction(unittest.TestCase):

    def setUp(self):
        self.mock_input = MagicMock()
        self.output = abstracts.create_callback_handler(self.mock_input)

    def test_is_subclass_Abstract_Handler(self):
        self.assertTrue(issubclass(self.output, abstracts.AbstractHandler))

    def test_handle_method_is_injected_method(self):
        self.assertEqual(self.mock_input, self.output.handle)

    def test_input_method_called_when_handle_called(self):
        self.output.handle()
        self.assertTrue(self.mock_input.called)


class MockCaller:

    def __init__(self, val):
        self.val = val
        self.destination_queue = MagicMock()

    @abstracts.handle_put_to_queue()
    def decorated_method(self):
        return self.val


class TestHandlePutToQueueDecorator(unittest.TestCase):

    def setUp(self):
        self.target_value = 'j46w5het'
        self.mock_caller = MockCaller(self.target_value)

    def test_calling_decorated_method_puts_returned_val_to_destination_queue(self):
        sub = self.mock_caller.destination_queue.put = MagicMock()
        self.mock_caller.decorated_method()
        self.assertTrue(sub.called)
        sub.assert_called_with(self.target_value)
