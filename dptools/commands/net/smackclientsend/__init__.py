"""
__init__.py	

Network SmackClientSend Command Package Module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from .smackclientsendcommand import (
    SmackClientSendCommand,
    SmackClientSendHandler,
    SmackClientSendResult
)


def register(callback_func):
    current = abstracts.create_callback_handler(callback_func)

    data = {
        SmackClientSendCommand.__name__: SmackClientSendHandler,
        SmackClientSendResult.__name__: current
    }
    return data
