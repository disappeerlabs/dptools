"""
toyapp.py	

Toy tkinter app for testing purposes

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import sys
import tkinter
from dptools.utilities import applogger
from dptools.tkcomponents.toyapp import toyappcontroller
from dptools.tkcomponents.toyapp import toyappview


class ToyApp:
    title = 'ToyApp'

    def __init__(self):
        self.title = self.title
        self.root = tkinter.Tk()
        self.log = self.config_logger()
        self.view = toyappview.ToyAppView(self.root)
        self.controller = toyappcontroller.ToyAppController(self.root, self.view)

    def config_logger(self):
        # TODO: enable logging to file, requires dirmaker to create files first
        # log_file = settings.default_log_file_path
        # log = applogger.AppLogger(self.title, file=log_file).create()
        log = applogger.AppLogger(self.title).create()
        sys.excepthook = log.handle_uncaught_system_exception
        # self.root.report_callback_exception = log.handle_uncaught_tkinter_exception
        return log

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log.info("Keyboard interrupt called. Shutting down.")
            sys.exit()


def main():
    app = ToyApp()
    app.run()


if __name__ == '__main__':
    main()
