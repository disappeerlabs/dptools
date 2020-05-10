"""
toyappcontroller.py	

> ENTER DESCRIPTION HERE

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import logging
from dptools.tkcomponents.toyapp import toyappview
from dptools.tkcomponents import debugwidget


class ToyAppController:

    def __init__(self, root):
        self.root = root
        self.root_view = toyappview.ToyAppView(self.root)
        self.log = logging.getLogger('ToyApp')
        self.debug_widget = debugwidget.initialize(self.root, self.root_view.main_frame)
        self.debug_widget.click_debug_2_override(self.override)

    def override(self, event):
        print("THIS IS THE OVERRIDE!!!!!")
