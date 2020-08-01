"""
smackserver.py	

Module for SmackServer and related classes.

SmackServer is the Single Message Ack Server:
    - listens for messages
    - responds with ACK
    - closes socket

>factory = smackserver.SmackServerFactory(None)
>server = factory.build()
>server.serve_forever()

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import socketserver
from dptools.commands import abstracts
from dptools.net.bases import abstractserverfactory
from dptools.net.protocols import ackprotocol
from dptools.commands.net.smackserverreceive.smackserverreceivecommand import SmackServerReceiveResult


class SmackServerFactory(abstractserverfactory.AbstractServerFactory):

    def __init__(self, queue, host='localhost', port=16661):
        super().__init__(queue)
        self.custom_host = host
        self.custom_port = port

    @property
    def name(self):
        return 'Smack_Server'

    @property
    def host(self):
        return self.custom_host

    @property
    def port(self):
        return self.custom_port

    @property
    def request_handler_obj(self):
        return SmackServerRequestHandler

    @property
    def server_obj(self):
        return ThreadedTCPServer


class SmackServerRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.destination_queue = self.server.queue
        self.protocol = ackprotocol.ACKProtocol(self.request)

    @abstracts.handle_put_to_queue()
    def handle(self):
        request = self.protocol.handle_request()
        # TODO: need to return result object that is particular to smack server
        #   - class could be in this module
        #   - module will then need a register function (cf. command pattern)
        #       - so that the result can be handled by queue consumer
        final = SmackServerReceiveResult(result=request)
        return final


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
