"""
test_queueconsumer.py

Test suite for QueueConsumer module and class object

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import queue
from unittest.mock import MagicMock, patch
from dptools.tkcomponents.baseapp import queueconsumer


class TestImportsAndVars(unittest.TestCase):

    def test_queue(self):
        self.assertEqual(queue, queueconsumer.queue)


class ConcreteQueueConsumer(queueconsumer.QueueConsumer):

    def __init__(self, root):
        super().__init__(root)
        self.log = MagicMock()

    def handle_queue_payload(self, payload):
        raise NotImplementedError

    def handle_queue_payload_error(self, payload):
        raise NotImplementedError

    def check_payload(self, payload):
        if not isinstance(payload, dict):
            self.log.error("{}-QueueConsumer payload of type {} is not dict: {}".format(type(self).__name__, type(payload), payload))
            return False
        try:
            desc = payload['desc']
        except KeyError as err:
            self.log.error("{}-QueueConsumer, malformed payload: {}, {}".format(type(self).__name__, err, payload))
            return False
        return payload


class TestQueueConsumerClassBasics(unittest.TestCase):

    def setUp(self):
        self.payload_dict = dict(desc='Test', data='wtf')
        self.payload_dict_bad = dict(data='wtf')
        self.root = MagicMock()
        self.x = ConcreteQueueConsumer(self.root)

    def test_instance(self):
        self.assertIsInstance(self.x, queueconsumer.QueueConsumer)

    def test_root_attribute_is_root(self):
        self.assertEqual(self.x.root, self.root)

    def test_queue_attribute_is_queue(self):
        self.assertIsInstance(self.x.queue, queue.Queue)

    #######################################
    #  POLLING AND QUEUE METHOD TESTS     #
    #######################################

    def test_process_queue_result_attribute(self):
        name = 'process_queue_result'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_process_queue_result_method_takes_dict(self):
        self.x.log.error = MagicMock()
        with self.assertRaises(NotImplementedError):
            result = self.x.process_queue_result('xxx666')
            self.assertTrue(self.x.log.error.called)

    def test_process_queue_result_method_error_on_no_dict(self):
        self.x.log.error = MagicMock()
        with self.assertRaises(NotImplementedError):
            result = self.x.process_queue_result('xxx666')
            self.assertTrue(self.x.log.error.called)

    def test_bad_payload_dict(self):
        self.x.log.error = MagicMock()
        with self.assertRaises(NotImplementedError):
            result = self.x.process_queue_result(self.payload_dict_bad)
            self.assertTrue(self.x.log.error.called)

    def test_consume_queue_attribute(self):
        name = 'consume_queue'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_consume_queue_method_with_queued_item(self):
        self.x.queue.put(self.payload_dict)
        self.x.process_queue_result = MagicMock()
        self.x.consume_queue()
        self.assertTrue(self.x.process_queue_result.called)

    def test_consume_queue_method_with_no_queued_item(self):
        self.x.process_queue_result = MagicMock()
        self.x.consume_queue()
        self.assertFalse(self.x.process_queue_result.called)

    def test_consume_queue_method_calls_get_queue(self):
        self.x.queue.put(self.payload_dict)
        self.x.queue.get = MagicMock(return_value=self.payload_dict)
        with self.assertRaises(NotImplementedError):
            self.x.consume_queue()
            self.assertTrue(self.x.queue.get.called)

    def test_consume_queue_method_calls_process_queue_with_got(self):
        self.x.process_queue_result = MagicMock()
        self.x.queue.put(self.payload_dict)
        self.x.consume_queue()
        self.x.process_queue_result.assert_called_with(self.payload_dict)

    def test_consume_queue_method_calls_task_done(self):
        self.x.queue.task_done = MagicMock()
        self.x.queue.put(self.payload_dict)
        with self.assertRaises(NotImplementedError):
            self.x.consume_queue()
            self.assertTrue(self.x.queue.task_done.called)

    def test_poll_queue_attribute(self):
        name = 'poll_queue'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_poll_queue_calls_consume_queue(self):
        self.x.consume_queue = MagicMock()
        self.x.poll_queue()
        self.assertTrue(self.x.consume_queue.called)

    def test_poll_queue_calls_root_after(self):
        self.x.root.after = MagicMock()
        self.x.poll_queue()
        self.assertTrue(self.x.root.after.called)

    def test_poll_queue_calls_root_after_with_args(self):
        self.x.root.after = MagicMock()
        self.x.poll_queue()
        self.x.root.after.assert_called_with(200,self.x.poll_queue)

    @patch.object(queueconsumer.QueueConsumer, 'poll_queue')
    def test_constructor_calls_poll_queue(self, mocked_method):
        x = queueconsumer.QueueConsumer(self.root)
        self.assertTrue(mocked_method.called)

    def test_check_payload_attribute(self):
        name = 'check_payload'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_check_payload_returns_valid_payload(self):
        result = self.x.check_payload(self.payload_dict)
        self.assertEqual(result, self.payload_dict)

    def test_handle_payload_attribute(self):
        name = 'handle_queue_payload'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_handle_payload_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.x.handle_queue_payload(self.payload_dict)

    def test_process_queue_result_calls_handle_payload_with_valid(self):
        with self.assertRaises(NotImplementedError):
            self.x.process_queue_result(self.payload_dict)

    def test_handle_payload_error_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.x.handle_queue_payload_error(self.payload_dict)

    def test_process_queue_result_calls_handle_queue_payload_error(self):
        sub = self.x.handle_queue_payload_error = MagicMock()
        self.x.process_queue_result(self.payload_dict_bad)
        sub.assert_called_with(self.payload_dict_bad)
