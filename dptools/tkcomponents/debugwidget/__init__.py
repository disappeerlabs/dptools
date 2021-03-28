"""
__init__.py	

Initializer for the debug frame widget

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.debugwidget.debugframe import DebugFrame as frame
from dptools.tkcomponents.debugwidget.debugcontroller import DebugController
name = 'Debug'


def register_widget(root, attach_view_method, attach_model_method, override_name=name):
    view = attach_view_method(frame, text=override_name)
    controller = DebugController(root, view, override_name)
    return controller


# TODO: remove this after refactoring dependencies
def register_widget_legacy(root, register_func, override_name=name):
    view = register_func(frame, text=override_name)
    controller = DebugController(root, view, override_name)
    return controller
