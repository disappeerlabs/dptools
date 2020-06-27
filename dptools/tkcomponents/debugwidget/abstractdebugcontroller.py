"""
abstractdebugcontroller.py	

Abstract base class for debug controller, subclass for varying implementations

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import abc
import logging


class AbstractDebugController(metaclass=abc.ABCMeta):

    def __init__(self, root, debug_view, app_title):
        self.root = root
        self.view = debug_view
        self.config_default_actions()
        self.log = logging.getLogger(app_title)

    def config_default_actions(self):
        self.view.config_event_bindings(self.click_debug_1_action, self.click_debug_2_action)

    #####################
    #  Abstract Methods #
    #####################

    @abc.abstractmethod
    def click_debug_1_action(self, event):
        raise NotImplementedError

    @abc.abstractmethod
    def click_debug_2_action(self, event):
        raise NotImplementedError

    #####################
    #  Override Methods #
    #####################

    def click_debug_1_override(self, func):
        self.view.button_1_bind(func)

    def click_debug_2_override(self, func):
        self.view.button_2_bind(func)

    ####################
    #  Textbox Methods #
    ####################

    def print_to_textbox(self, msg):
        self.view.print_to_debug(msg)

    def append_to_textbox(self, msg):
        self.view.append_to_debug(msg)

    def get_text_from_textbox(self):
        return self.view.get_text()
