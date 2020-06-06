"""
createnewkeycommand.py	

Class objects for create new key command pattern

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts


class CreateNewKeyCommand(abstracts.AbstractCommand):
    def __init__(self, key_dir_path=None, key_input_dict=None):
        super().__init__(key_dir_path=key_dir_path, key_input_dict=key_input_dict)


class CreateNewKeyHandler(abstracts.AbstractHandler):
    pass


class CreateNewKeyResult(abstracts.AbstractResult):
    pass

