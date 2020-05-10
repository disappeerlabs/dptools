"""
toyappcontroller.py	

> ENTER DESCRIPTION HERE

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import logging
from dptools.tkcomponents import debugwidget


class ToyAppController:

    def __init__(self, root, root_view):
        self.root = root
        self.log = logging.getLogger('ToyApp')
        self.root_view = root_view
        self.debug_widget = debugwidget.initialize(self.root_view.main_frame)
