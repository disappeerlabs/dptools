"""
checksanitycommand.py	

Check Sanity Command Pattern objects

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