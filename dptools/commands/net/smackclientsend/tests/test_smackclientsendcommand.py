"""
test_smackclientsendcommand.py	

Tests for the smack client send command module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from dptools.commands.tests import baseclasstestcommandpattern
from dptools.commands.net import smackclientsend
from dptools.commands.net.smackclientsend.smackclientsendcommand import (
    SmackClientSendCommand,
    SmackClientSendHandler,
    SmackClientSendResult
)

patch_path_string = 'dptools.commands.net.smackclientsend.smackclientsendcommand.SmackClient'


@patch(patch_path_string)
class TestSmackClientSendCommand(baseclasstestcommandpattern.BaseClassTestCommandPattern):

    host = 'localhost'
    port = '1234'
    command = 'ACK'
    payload_dict = dict(msg='Hello')
    proxy_arg = False

    def config_register_callback(self):
        return smackclientsend.register(self.mock_callback)

    def config_command(self):
        command = SmackClientSendCommand(host=self.host,
                                         port=self.port,
                                         command=self.command,
                                         payload_dict=self.payload_dict,
                                         proxy=self.proxy_arg)
        return command

    def command_class(self):
        return SmackClientSendCommand

    def handler_class(self):
        return SmackClientSendHandler

    def result_class(self):
        return SmackClientSendResult

    def test_command_attr_host(self, *args):
        target = self.config_command()
        self.assertEqual(self.host, target.host)

    def test_command_attr_port(self, *args):
        target = self.config_command()
        self.assertEqual(self.port, target.port)

    def test_command_attr_command(self, *args):
        target = self.config_command()
        self.assertEqual(self.command, target.command)

    def test_command_attr_payload_dict(self, *args):
        target = self.config_command()
        self.assertEqual(self.payload_dict, target.payload_dict)

    def test_handler_handle_method_returns_result_from_client_send(self, mock_client):
        result = 'Hello there'
        config_method = mock_client().configure_transport = MagicMock(return_value=None)
        send_method = mock_client().send = MagicMock(return_value=result)
        result_obj = self.helper_get_result_from_queue()
        self.assertEqual(result_obj.result, result)

    def test_handler_handle_method_calls_config_transport_with_proxy_arg(self, mock_client):
        result = 'Hello there'
        config_method = mock_client().configure_transport = MagicMock(return_value=None)
        send_method = mock_client().send = MagicMock(return_value=result)
        result_obj = self.helper_get_result_from_queue()
        self.assertTrue(config_method.called)
        config_method.assert_called_with(proxy=self.proxy_arg)

    def test_handler_handle_method_returns_config_transport_error(self, mock_client):
        result = 'Hello there'
        config_result = MagicMock()
        config_method = mock_client().configure_transport = MagicMock(return_value=config_result)
        send_method = mock_client().send = MagicMock(return_value=result)
        result_obj = self.helper_get_result_from_queue()
        self.assertEqual(result_obj.result, config_result)
        self.assertEqual(result_obj.result.name, self.handler_class().__name__)
