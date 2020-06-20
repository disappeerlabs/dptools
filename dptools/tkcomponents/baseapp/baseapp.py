"""
baseapp.py

Base tkinter app for testing purposes

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import sys
import tkinter
from dptools.utilities.applogger import AppLogger


class BaseApp:

    def __init__(self, controller_class, title='BaseApp'):
        self.title = title
        self.root = tkinter.Tk()
        self.root.title(self.title)
        self.log = self.config_logger()
        self.controller = controller_class(self.root)

    def config_logger(self):
        log = AppLogger(AppLogger.name).create()
        sys.excepthook = log.handle_uncaught_system_exception
        self.root.report_callback_exception = log.handle_uncaught_tkinter_exception
        return log

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log.info("Keyboard interrupt called. Shutting down.")
            sys.exit()
