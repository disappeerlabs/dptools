"""
deletekeycommand.py	

Classes for delete key command implementation

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from dptools.gpg.agents.keydeleter import KeyDeleter


class DeleteKeyCommand(abstracts.AbstractCommand):
    def __init__(self, key_dir_path=None, key_fingerprint_list=None, secret=None, passphrase=None):
        super().__init__(key_dir_path=key_dir_path, key_fingerprint_list=key_fingerprint_list, secret=secret, passphrase=passphrase)


class DeleteKeyHandler(abstracts.AbstractHandler):

    @abstracts.handle_put_to_queue()
    def handle(self, command: DeleteKeyCommand):
        agent = KeyDeleter(command.key_dir_path)
        result = agent.execute(command.key_fingerprint_list,
                               secret=command.secret,
                               passphrase=command.passphrase)
        result_obj = DeleteKeyResult(result=result)
        return result_obj


class DeleteKeyResult(abstracts.AbstractResult):
    pass
