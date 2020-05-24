"""
ackprotocol.py

Module for the ACKProtocol class object.

ACK Protocol:
    - client calls send_request and handle_response
    - server calls handle_request
    - if client request is valid (has payload with ack string):
        - server responds by echoing payload with ack, closes socket
    - if client request is not valid
        - server closes socket

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.net.bases import baseprotocol


class ACKProtocol(baseprotocol.BaseProtocol):

    def __init__(self, sock):
        super().__init__(sock)

    def send_request(self, payload_dict, command_string):
        packet = self.build_packet(payload_dict, command_string)
        self.sock.sendall(packet)

    def handle_request(self):
        request = self.process_incoming(self.ack_string)
        if request:
            self.send_ack(request)
        else:
            self.sock.close()
        return request

    def handle_response(self):
        payload = self.process_incoming(self.ack_string)
        self.sock.close()
        return payload

    def send_ack(self, payload_dict):
        packet = self.build_packet(payload_dict, self.ack_string)
        self.sock.sendall(packet)
        self.sock.close()
