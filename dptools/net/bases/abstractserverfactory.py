"""
abstractserverfactory.py

Abstract base class for server factories

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import abc


class AbstractServerFactory(metaclass=abc.ABCMeta):
    Server_Error = 'Server_Error'

    def __init__(self, queue):
        self.queue = queue

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def host(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def port(self):
        raise NotImplementedError

    @property
    def interface(self):
        return self.host, self.port

    @property
    @abc.abstractmethod
    def request_handler_obj(self):
        # TODO: this is misnamed, returns class not object
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def server_obj(self):
        # TODO: this is misnamed, returns class not object
        raise NotImplementedError

    def build(self):
        try:
            server = self.server_obj(self.interface, self.request_handler_obj)
        except OSError as err:
            # TODO: replace this raw dict with proper consumable?
            error_dict = dict(desc=self.Server_Error,
                              error=err,
                              interface=self.interface)
            self.queue.put(error_dict)
            return None
        server.queue = self.queue
        return server
