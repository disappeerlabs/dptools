"""
abstracts.py	

Command abstractions

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import abc


class AbstractCommand(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.__dict__.update(kwargs)


class AbstractHandler(metaclass=abc.ABCMeta):

    def __init__(self, destination_queue):
        self.destination_queue = destination_queue

    @abc.abstractmethod
    def handle(self, command: AbstractCommand):
        raise NotImplementedError


class AbstractResult(metaclass=abc.ABCMeta):

    def __init__(self, result):
        self.name = self.__class__.__name__
        self.result = result


class TempHandler(AbstractHandler):
    def __init__(self, *args):
        super().__init__(*args)

    def handle(self, command):
        pass


def create_callback_handler(callback_function):
    current = TempHandler
    current.handle = callback_function
    return current
