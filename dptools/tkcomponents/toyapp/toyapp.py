"""
toyapp.py	

Toy tkinter app for testing purposes

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import sys
import argparse
import tkinter
from dptools.utilities.applogger import AppLogger
from dptools.tkcomponents.toyapp.controllers import basictoyappcontroller, queuetoyappcontroller


class ToyApp:
    # Todo: add docs for toyapp
    title = 'ToyApp'

    def __init__(self, controller_class):
        self.title = self.title
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--queue', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.queue:
        controller_class = queuetoyappcontroller.QueueToyAppController
    else:
        controller_class = basictoyappcontroller.BasicToyAppController

    app = ToyApp(controller_class)
    app.run()


if __name__ == '__main__':
    main()
