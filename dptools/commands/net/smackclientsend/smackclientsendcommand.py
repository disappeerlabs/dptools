"""
smackclientsendcommand.py	

Command module for Smack Client Send functionality

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from dptools.net.smack.smackclient import SmackClient


class SmackClientSendCommand(abstracts.AbstractCommand):
    def __init__(self, host=None, port=None, command=None, payload_dict=None, proxy=None):
        super().__init__(host=host, port=port, command=command, payload_dict=payload_dict, proxy=proxy)


class SmackClientSendHandler(abstracts.AbstractHandler):

    @abstracts.handle_put_to_queue()
    def handle(self, command: SmackClientSendCommand):
        client = SmackClient(command)
        error_status = client.configure_transport(proxy=command.proxy)
        if error_status is not None:
            error_status.name = self.__class__.__name__
            response = error_status
        else:
            response = client.send()
        return SmackClientSendResult(response)


class SmackClientSendResult(abstracts.AbstractResult):
    def __init__(self, result):
        super().__init__(result)
