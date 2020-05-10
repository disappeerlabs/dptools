"""
__init__.py	

Initializer for the debug frame widget

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.debugwidget import debugcontroller


def initialize(root, parent_widget):
    d = debugcontroller.DebugController(root, parent_widget, 'ToyApp')
    return d
