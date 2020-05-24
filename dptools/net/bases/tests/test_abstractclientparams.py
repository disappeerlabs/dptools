"""
test_abstractclientparams.py	

Tests for AbstractClientParams object.
A dataclass to encapsulate params for Abstract Client Config

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import queue
from dptools.net.bases.abstractclientparams import AbstractClientParams


class TestAbstractClientParamsBasic(unittest.TestCase):

    def setUp(self):
        self.host = 'host'
        self.port = 4567
        self.queue = MagicMock(spec=queue.Queue)
        self.nonce = 'nonce_string'
        self.payload_dict = dict(hello='hello')
        self.command = 'command_string'
        self.x = AbstractClientParams(self.host,
                                      self.port,
                                      self.command,
                                      self.payload_dict)

    def test_host_property(self):
        result = self.x.host
        self.assertEqual(result, self.host)

    def test_port_property(self):
        result = self.x.port
        self.assertEqual(result, self.port)

    def test_payload_dict_property(self):
        self.assertEqual(self.x.payload_dict, self.payload_dict)

    def test_command_property(self):
        result = self.x.command
        self.assertEqual(result, self.command)
