"""
createnewkeycommand.py	

Class objects for create new key command pattern

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts
from dptools.commands.abstracts import AbstractCommand
from dptools.gpg.agents.gpgagent import GPGAgent


class CreateNewKeyCommand(abstracts.AbstractCommand):
    def __init__(self, key_dir_path=None, key_input_dict=None):
        super().__init__(key_dir_path=key_dir_path, key_input_dict=key_input_dict)


class CreateNewKeyHandler(abstracts.AbstractHandler):

    @abstracts.handle_put_to_queue()
    def handle(self, command: AbstractCommand):
        agent = GPGAgent(command.key_dir_path)
        input_data = agent.gpg.gen_key_input(**command.key_input_dict)
        result = agent.gpg.gen_key(input_data)
        result_obj = CreateNewKeyResult(result=result)
        return result_obj


class CreateNewKeyResult(abstracts.AbstractResult):
    def __init__(self, result):
        super().__init__(result)
