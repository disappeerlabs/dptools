"""
__init__.py	

Check Sanity Exploratory Concrete Command Implementation
    - pattern presumes registration with QueueConsumer

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts


class CheckSanityCommand(abstracts.AbstractCommand):

    def __init__(self, message=None):
        super().__init__(message=message)


class CheckSanityHandler(abstracts.AbstractHandler):

    def handle(self, command: CheckSanityCommand):
        result = command.message
        result_obj = CheckSanityResult(result=result)
        self.destination_queue.put(result_obj)


class CheckSanityResult(abstracts.AbstractResult):

    def __init__(self, result):
        super().__init__(result)


def register_key_map(callback_func):
    current = abstracts.create_callback_handler(callback_func)

    data = {
        CheckSanityCommand.__name__: CheckSanityHandler,
        CheckSanityResult.__name__: current
    }
    return data
