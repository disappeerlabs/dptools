"""
__init__.py

alertbox popup widget init module
    - import the alertbox package
    - call initialize on it, with the required args for AlertBoxController


Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.popuplauncher.alertbox import alertboxcontroller


def initialize(*args):
    return alertboxcontroller.AlertBoxController(*args)
