"""
basecontroller.py	

Base controller class subclassed by concrete implementations

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import logging
from dptools.tkcomponents.toyapp import toyappview
from dptools.tkcomponents import debugwidget
from dptools.utilities.applogger import AppLogger


class BaseController:

    def __init__(self, root):
        self.root = root
        self.root_view = toyappview.ToyAppView(self.root)
        self.log = logging.getLogger(AppLogger.name)
        self.debug_widget = debugwidget.initialize(self.root, self.root_view.main_frame)
