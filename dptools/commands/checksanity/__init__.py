"""
__init__.py	

Check Sanity Exploratory Concrete Command Implementation
    - pattern presumes registration with QueueConsumer

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from .checksanitycommand import (
    CheckSanityCommand,
    CheckSanityHandler,
    CheckSanityResult
)


def register(callback_func):
    current = abstracts.create_callback_handler(callback_func)

    data = {
        CheckSanityCommand.__name__: CheckSanityHandler,
        CheckSanityResult.__name__: current
    }
    return data
