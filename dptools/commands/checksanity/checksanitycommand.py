"""
checksanitycommand.py	

Check Sanity Command Pattern objects

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from dptools.commands.abstracts import (
    AbstractCommand,
    AbstractHandler,
    AbstractResult
)


class CheckSanityCommand(AbstractCommand):

    def __init__(self, message=None):
        super().__init__(message=message)


class CheckSanityHandler(AbstractHandler):

    @abstracts.handle_put_to_queue()
    def handle(self, command: CheckSanityCommand):
        result = command.message
        result_obj = CheckSanityResult(result=result)
        return result_obj


class CheckSanityResult(AbstractResult):

    def __init__(self, result):
        super().__init__(result)
