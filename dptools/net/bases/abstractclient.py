"""
abstractclient.py

Module for the AbstractClient base class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import abc
import socket
import socks


class AbstractClient(metaclass=abc.ABCMeta):

    def __init__(self, client_params):
        self.client_params = client_params
        self.sock = None
        self.protocol = None
        self.error = None

    @property
    def host(self):
        return self.client_params.host

    @property
    def port(self):
        return self.client_params.port

    @property
    def interface(self):
        return self.host, self.port

    @property
    def payload_dict(self):
        return self.client_params.payload_dict

    @property
    def command(self):
        return self.client_params.command

    def create_socket(self, proxy=True):
        """
        Proxy by default, kwarg toggles use of presumed Tor proxy on port 9050 on localhost.
        If proxy is False, then return standard socket without proxy.
        :param proxy: bool
        :return: socket
        """
        if proxy:
            self.sock = socks.socksocket()
            self.sock.set_proxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050, True)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.settimeout(10)
        return self.sock

    def connect(self):
        self.sock.connect(self.interface)

    @abc.abstractmethod
    def wrap_socket(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_protocol(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError

    @abc.abstractmethod
    def handle_response(self):
        raise NotImplementedError

    def stop(self):
        self.sock.close()

    def configure_transport(self, proxy=True):
        try:
            self.create_socket(proxy=proxy)
            self.connect()
            self.wrap_socket()
        except (socket.error, ConnectionRefusedError) as err:
            self.error = err
            return err
        self.set_protocol()
