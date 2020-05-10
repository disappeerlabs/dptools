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

# Todo: add docs for toyapp

class ToyApp:
    title = 'ToyApp'

    def __init__(self):
        self.title = self.title
        self.root = tkinter.Tk()
        self.log = self.config_logger()
        self.controller = toyappcontroller.ToyAppController(self.root)

    def config_logger(self):
        log = applogger.AppLogger(self.title).create()
        sys.excepthook = log.handle_uncaught_system_exception
        self.root.report_callback_exception = log.handle_uncaught_tkinter_exception
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
