"""
detachedverifier.py

Module for DetachedVerifier class object

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.gpg.agents import gpgagent


class DetachedVerifier(gpgagent.GPGAgent):

    def __init__(self, keydir):
        super().__init__(keydir)

    def execute(self, path_to_sig_file, data_bytestring):
        result = self.gpg.verify_data(path_to_sig_file, data_bytestring)
        return result

