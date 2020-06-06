"""
__init__.py	

Create New Key command init

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from .createnewkeycommand import (
    CreateNewKeyCommand,
    CreateNewKeyHandler,
    CreateNewKeyResult
)


def register(callback_func):
    current = abstracts.create_callback_handler(callback_func)

    data = {
        CreateNewKeyCommand.__name__: CreateNewKeyHandler,
        CreateNewKeyResult.__name__: current
    }
    return data
