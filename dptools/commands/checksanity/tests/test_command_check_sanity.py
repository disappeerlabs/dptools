"""
test_command_check_sanity.py	

Tests for the check sanity command implementation

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands.tests import baseclasstestcommandpattern
from dptools.commands import checksanity
from dptools.commands.checksanity.checksanitycommand import (
    CheckSanityCommand,
    CheckSanityHandler,
    CheckSanityResult
)


class TestCheckSanityWithBaseClass(baseclasstestcommandpattern.BaseClassTestCommandPattern):

    def config_register_callback(self):
        return checksanity.register(self.mock_callback)

    def config_command(self):
        self.msg = "Hello there"
        command = CheckSanityCommand(self.msg)
        return command

    def command_class(self):
        return CheckSanityCommand

    def handler_class(self):
        return CheckSanityHandler

    def result_class(self):
        return CheckSanityResult

    def setUp(self):
        super().setUp()

    def test_handling_command_from_command_map_returns_result_with_msg(self):
        result_obj = self.helper_get_result_from_queue()
        # Result should be original message, specific to this command
        self.assertEqual(result_obj.result, self.msg)
