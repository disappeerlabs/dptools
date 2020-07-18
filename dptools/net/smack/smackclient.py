"""
smackclient.py	

Module for SmackClient class

params = SimpleNamespace()
params.host = host
params.port = port
params.command = command
params.payload_dict = payload_dict
c = SmackClient(self.params)
response = c.send()

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.net.bases import abstractclient
from dptools.net.protocols import ackprotocol


class SmackClient(abstractclient.AbstractClient):

    def set_protocol(self):
        self.protocol = ackprotocol.ACKProtocol(self.sock)

    def send(self):
        try:
            self.protocol.send_request(self.payload_dict, self.command)
        except (BrokenPipeError, OSError) as err:
            output = err
        else:
            output = self.handle_response()
        return output

    def handle_response(self):
        try:
            output = self.protocol.handle_response()
        except ConnectionResetError as err:
            output = err
        # TODO: add put to queue or remove queue from setup
        return output

    def wrap_socket(self):
        pass
