"""
__init__.py	

SmackServerReceive: command package to handle receiving a result from smack server

This is a partial implementation of the command pattern.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from .smackserverreceivecommand import (
    SmackServerReceiveResult
)


def register(callback_func):
    current = abstracts.create_callback_handler(callback_func)
    data = {
        SmackServerReceiveResult.__name__: current
    }
    return data
