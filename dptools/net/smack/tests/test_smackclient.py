"""
test_smackclient.py	

Tests for SMAck Client module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from types import SimpleNamespace
from dptools.net.smack import smackclient
from dptools.net.bases import abstractclient
from dptools.net.protocols import ackprotocol


class TestSmackClient(unittest.TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.port = 16661
        self.command = 'ACK'
        self.payload_dict = dict(msg='Hello world')
        self.params = SimpleNamespace()
        self.params.host = self.host
        self.params.port = self.port
        self.params.command = self.command
        self.params.payload_dict = self.payload_dict
        self.x = smackclient.SmackClient(self.params)

    def test_instance(self):
        self.assertIsInstance(self.x, smackclient.SmackClient)

    def test_instance_abstract_client(self):
        self.assertIsInstance(self.x, abstractclient.AbstractClient)

    def test_client_attrs_are_set(self):
        self.assertEqual(self.x.host, self.host)
        self.assertEqual(self.x.port, self.port)
        self.assertEqual(self.x.command, self.command)
        self.assertEqual(self.x.payload_dict, self.payload_dict)

    def test_set_protocol_sets_ack_protocol(self):
        self.x.set_protocol()
        self.assertIsInstance(self.x.protocol, ackprotocol.ACKProtocol)

    def test_send_method_calls_send_request_on_protocol(self):
        self.x.protocol = MagicMock(spec=ackprotocol.ACKProtocol)
        self.x.send()
        self.x.protocol.send_request.assert_called_with(self.x.payload_dict, self.x.command)

    def test_send_method_catches_broken_pipe_error(self):
        self.x.protocol = MagicMock(spec=ackprotocol.ACKProtocol)
        self.x.protocol.send_request.side_effect = BrokenPipeError
        result = self.x.send()
        self.assertIsInstance(result, BrokenPipeError)

    def test_send_method_catches_os_error(self):
        self.x.protocol = MagicMock(spec=ackprotocol.ACKProtocol)
        self.x.protocol.send_request.side_effect = OSError
        result = self.x.send()
        self.assertIsInstance(result, OSError)

    def test_send_method_returns_handle_response_output_no_error(self):
        target_val = 'hello there'
        self.x.protocol = MagicMock(spec=ackprotocol.ACKProtocol)
        self.x.protocol.handle_response.return_value = target_val
        result = self.x.send()
        self.assertEqual(result, target_val)

    def test_handle_response_returns_result_from_protocol_handle_response(self):
        target_val = 'handle_response_output'
        self.x.protocol = MagicMock(spec=ackprotocol.ACKProtocol)
        self.x.protocol.handle_response.return_value = target_val
        result = self.x.handle_response()
        self.assertEqual(target_val, result)

    def test_handle_response_catches_connection_reset_error(self):
        self.x.protocol = MagicMock(spec=ackprotocol.ACKProtocol)
        self.x.protocol.handle_response.side_effect = ConnectionResetError
        result = self.x.handle_response()
        self.assertIsInstance(result, ConnectionResetError)
