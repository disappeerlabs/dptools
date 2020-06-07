"""
__init__.py	

GPG Delete Key Command init

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from .deletekeycommand import (
    DeleteKeyCommand,
    DeleteKeyHandler,
    DeleteKeyResult
)


def register(callback_func):
    current = abstracts.create_callback_handler(callback_func)

    data = {
        DeleteKeyCommand.__name__: DeleteKeyHandler,
        DeleteKeyResult.__name__: current
    }
    return data

