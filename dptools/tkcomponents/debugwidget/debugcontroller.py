"""
debugcontroller.py	

Controller for Debug Widget

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import logging
from dptools.tkcomponents.debugwidget import debugframe


class DebugController:

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
    #  Button 1 Methods #
    #####################

    def click_debug_1_action(self, event):
        self.log.debug("Debug button 1 clicked")

        from dptools.tkcomponents.popuplauncher import launch_popup, alertbox
        r = launch_popup(alertbox, self.root, "is this thing on?")
        self.append_to_textbox("Hello there")

    def click_debug_1_override(self, func):
        self.view.button_1_bind(func)

    #####################
    #  Button 2 Methods #
    #####################

    def click_debug_2_action(self, event):
        self.log.debug("Debug button 2 clicked")
        self.print_to_textbox('')

    def click_debug_2_override(self, func):
        self.view.button_2_bind(func)

    ####################
    #  Textbox Methods #
    ####################

    def print_to_textbox(self, msg):
        self.view.print_to_debug(msg)

    def append_to_textbox(self, msg):
        self.view.append_to_debug(msg)
