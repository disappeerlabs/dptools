"""
keydeleter.py

Module for KeyDeleter class object

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.gpg.agents import gpgagent


class KeyDeleter(gpgagent.GPGAgent):

    def __init__(self, keydir):
        super().__init__(keydir)

    def execute(self, key_fingerprint_list, secret=False, passphrase=None):
        # TODO: manually confirm proper functioning of deletion after UI is built
        if secret and passphrase:
            prep = self.gpg.delete_keys(key_fingerprint_list, secret=secret, passphrase=passphrase)
            result = self.gpg.delete_keys(key_fingerprint_list)
        else:
            result = self.gpg.delete_keys(key_fingerprint_list)
        return result
