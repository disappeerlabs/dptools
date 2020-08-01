"""
test_smackserver.py	

Test module for smackserver implementation.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
import socketserver
from dptools.net.smack import smackserver
from dptools.net.bases import abstractserverfactory
from dptools.net.protocols import ackprotocol
from dptools.commands.net.smackserverreceive.smackserverreceivecommand import SmackServerReceiveResult


class TestSmackServerFactory(unittest.TestCase):

    def setUp(self):
        self.name = 'Smack_Server'
        self.host_default = 'localhost'
        self.host_alt = '0.0.0.0'
        self.port_default = 16661
        self.port_alt = 1234
        self.queue = MagicMock()
        self.x = smackserver.SmackServerFactory(self.queue)
        self.alt_x = smackserver.SmackServerFactory(self.queue,
                                                    host=self.host_alt,
                                                    port=self.port_alt)

    def test_class_instance(self):
        self.assertIsInstance(self.x, smackserver.SmackServerFactory)

    def test_instance_abstractserverfactory(self):
        self.assertIsInstance(self.x, abstractserverfactory.AbstractServerFactory)

    def test_queue_attr_set(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_factory_name(self):
        self.assertEqual(self.name, self.x.name)

    def test_host_default(self):
        self.assertEqual(self.x.host, self.host_default)

    def test_port_default(self):
        self.assertEqual(self.x.port, self.port_default)

    def test_host_custom(self):
        self.assertEqual(self.alt_x.host, self.host_alt)

    def test_port_custom(self):
        self.assertEqual(self.alt_x.port, self.port_alt)

    def test_server_obj_property(self):
        target = smackserver.ThreadedTCPServer
        self.assertEqual(target, self.x.server_obj)

    def test_request_handler_property(self):
        target = smackserver.SmackServerRequestHandler
        self.assertEqual(target, self.x.request_handler_obj)


class TestSmackServerRequestHandler(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.client_address = MagicMock()
        self.server = MagicMock()
        self.mocked_protocol = smackserver.ackprotocol.ACKProtocol = MagicMock(spec=ackprotocol.ACKProtocol(self.request))
        self.x = smackserver.SmackServerRequestHandler(self.request, self.client_address, self.server)

    def test_class_instnce(self):
        self.assertIsInstance(self.x, smackserver.SmackServerRequestHandler)

    def test_BaseRequestHandler_instance(self):
        self.assertIsInstance(self.x, socketserver.BaseRequestHandler)

    def test_has_handle_method(self):
        check = hasattr(smackserver.SmackServerRequestHandler, 'handle')
        self.assertTrue(check)

    @patch('dptools.net.protocols.ackprotocol.ACKProtocol')
    def test_setup_method_calls_and_sets_act_protocol(self, target):
        self.x.setup()
        self.assertTrue(target.called)
        self.assertEqual(self.x.protocol, target.return_value)

    @patch('dptools.net.protocols.ackprotocol.ACKProtocol')
    def test_setup_method_sets_destination_queue(self, target):
        self.x.setup()
        self.assertEqual(self.x.destination_queue, self.x.server.queue)

    def test_handle_method_calls_handle_on_protocol_and_returns_val_in_smack_result(self):
        val = 'mock_return_value_string'
        self.x.protocol.handle_request = MagicMock(return_value=val)
        result = self.x.handle()
        self.assertTrue(self.x.protocol.handle_request.called)
        self.assertEqual(val, result.result)
        self.assertIsInstance(result, SmackServerReceiveResult)

    @patch('dptools.net.protocols.ackprotocol.ACKProtocol')
    def test_handle_method_return_val_is_put_to_queue(self, target):
        self.x.setup()
        mock_queue_method = self.x.destination_queue.put = MagicMock()
        val = 'mock_return_value_string'
        self.x.protocol.handle_request = MagicMock(return_value=val)
        result = self.x.handle()
        self.assertTrue(self.x.protocol.handle_request.called)
        self.assertEqual(val, result.result)
        self.assertIsInstance(result, SmackServerReceiveResult)
        self.assertTrue(mock_queue_method.called)


class TestThreadedTCPServerBasics(unittest.TestCase):

    def setUp(self):
        self.server_address = MagicMock()
        self.req_handler_class = MagicMock()
        self.x = smackserver.ThreadedTCPServer
        self.base_list = self.x.__bases__

    def test_class_object(self):
        self.assertEqual(self.x, smackserver.ThreadedTCPServer)

    def test_threading_mixin_base(self):
        self.assertIn(socketserver.ThreadingMixIn, self.base_list)

    def test_tcpserver_base(self):
        self.assertIn(socketserver.TCPServer, self.base_list)

    def test_allow_reuse_address_true(self):
        self.assertTrue(self.x.allow_reuse_address)


