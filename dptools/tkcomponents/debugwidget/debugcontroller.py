"""
debugcontroller.py	

> ENTER DESCRIPTION HERE

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

        self.config_actions()
        self.log = logging.getLogger(app_title)

    def config_actions(self):
        self.view.config_event_bindings(self.click_debug_1_action, self.click_debug_2_action)

    def click_debug_1_action(self, event):
        self.log.debug("Debug button 1 clicked")
        self.log.debug(dir(event.widget))

        from dptools.tkcomponents import popuplauncher
        from dptools.tkcomponents.popuplauncher import alertbox
        r = popuplauncher.launch_popup(alertbox, self.root, "is this thing on?")

    def click_debug_2_action(self, event):
        self.log.debug("Debug button 2 clicked")
