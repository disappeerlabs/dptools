"""
__init__.py	

Initializer for the debug frame widget

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.debugwidget.debugframe import DebugFrame as frame
from dptools.tkcomponents.debugwidget.debugcontroller import DebugController
name = 'Debug'


def register_widget(root, register_func, override_name=name):
    view = register_func(frame, text=override_name)
    controller = DebugController(root, view, override_name)
    return controller
