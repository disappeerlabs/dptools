"""
notebookview.py

Notebook view object for root panel

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from dptools.static import styling


class RootPanelView:
    """
    Main left panel view for root window
    """

    def __init__(self, parent):
        self.parent = parent

        # Init accessible instance attributes
        self.main_frame = None
        self.notebook = None

        self.style = ttk.Style()
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_notebook()
        self.parent.add(self.main_frame)

    def config_main_frame(self):
        """
        Main outermost frame for left panel.
        """
        self.main_frame = tkinter.Frame(self.parent, background=styling.background_color)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def config_notebook(self):
        """
        Configure ttk notebook widget and call methods for its tab widgets
        """
        self.notebook = ttk.Notebook(self.main_frame, padding=(10, 5, 10, 10))
        self.notebook.grid(row=0, column=0, sticky=styling.sticky_all)

    def add_tab_to_notebook(self, frame_class, **kwargs):
        frame_object = frame_class(self.notebook)
        self.notebook.add(frame_object, **kwargs)
        return frame_object
