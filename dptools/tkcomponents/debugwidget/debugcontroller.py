"""
debugcontroller.py	

Controller for Debug Widget

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.debugwidget import abstractdebugcontroller


class DebugController(abstractdebugcontroller.AbstractDebugController):

    def __init__(self, root, parent_widget, app_title):
        super().__init__(root, parent_widget, app_title)

    def config_default_actions(self):
        self.view.config_event_bindings(self.click_debug_1_action, self.click_debug_2_action)

    #####################################
    #  Implement Abstract Click Methods #
    #####################################

    def click_debug_1_action(self, event):
        self.log.debug("Debug button 1 clicked")

        from dptools.tkcomponents.popuplauncher import launch_popup, alertbox
        r = launch_popup(alertbox, self.root, "is this thing on?")
        self.append_to_textbox("Hello there")

    def click_debug_2_action(self, event):
        self.log.debug("Debug button 2 clicked")
        self.print_to_textbox('')
