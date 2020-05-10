"""
constants.py	

dptools constants file

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import collections

# To add a new constant to the command list, add string to inputs
command_list_inputs = ['Check_Sanity',
                       'Create_New_Key']
command_list_tuple_obj = collections.namedtuple("Command_List", command_list_inputs)
command_list = command_list_tuple_obj(*command_list_inputs)
