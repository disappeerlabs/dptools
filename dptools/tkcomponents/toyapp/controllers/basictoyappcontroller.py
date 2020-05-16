"""
basictoyappcontroller.py

Controller class for toy app

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.toyapp.controllers import basecontroller


class BasicToyAppController(basecontroller.BaseController):

    def __init__(self, root):
        super().__init__(root)
        self.debug_widget.click_debug_2_override(self.override)

    def override(self, event):
        print("THIS IS THE OVERRIDE!!!!!")
