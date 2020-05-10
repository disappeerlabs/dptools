"""
toyappview.py	

Root view for the toy app tkinter GUI

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import tkinter
from dptools.static import styling


class ToyAppView:
    """
    Root view for disappeer root controller
    """
    def __init__(self, root):
        # Configure root
        self.root = root
        self.root.minsize(200, 200)
        self.root.title('ToyApp')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Run setup
        styling.config_ttk_styling()
        self.main_frame = self.config_main_frame()

        # Set focus
        self.root.focus()

    def config_main_frame(self):
        """
        Configure the main outer frame for the main view
        """
        main_frame = tkinter.Frame(self.root, background=styling.background_color)
        main_frame.grid(column=0, row=0, sticky=styling.sticky_all)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.add_widget_to_grid = lambda widget: widget.grid(row=0, column=0, sticky=styling.sticky_all)
        return main_frame
