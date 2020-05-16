"""
abstractdebugcontroller.py	

Abstract base class for debug controller, subclass for varying implementations

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import abc
import logging
from dptools.tkcomponents.debugwidget import debugframe


class AbstractDebugController(metaclass=abc.ABCMeta):

    def __init__(self, root, parent_widget, app_title):
        self.root = root
        self.parent_widget = parent_widget

        # Instantiate the view/frame with parent widget as parent
        self.view = debugframe.DebugFrame(parent_widget)

        # Add the widget to the parent
        self.parent_widget.add_widget_to_grid(self.view)

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
