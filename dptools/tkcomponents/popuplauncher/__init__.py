"""
__init__.py	

init module for the popuplaucher package:
    - import the popuplaucher package as a module
    - call lauch_popup on it
    - pass in the requisite args

>from dptools.tkcomponents.popuplauncher import launch_popup, alertbox
>r = launch_popup(alertbox, self.root, "is this thing on?")

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""


def launch_popup(popup_widget, *args):
    # TODO: add tests for this functionality
    """
    :param popup_widget: the package module for the target popup you wish to launch
    :param args: popup_widget package/
    :return: result of window.show(), the output defined on the popup controller
    """
    window = popup_widget.initialize(*args)
    result = window.show()
    return result
