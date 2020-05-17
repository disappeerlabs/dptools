"""
threaddispatcher.py	

Simple Concrete Handler Wrapper to dispatch command execution to thread.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import threading
from dptools.commands.abstracts import AbstractHandler


class ThreadDispatchDecorator(AbstractHandler):

    def __init__(self, destination_queue, decorated_handler):
        super().__init__(destination_queue)
        self.decorated = decorated_handler

    def handle(self, command):
        self.dispatch(self.decorated.handle, command)

    def dispatch(self, func, command):
        t = threading.Thread(name=command.name,
                             target=func,
                             args=(command,))
        t.start()
