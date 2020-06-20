"""
basepanelview.py

Base panel view for base controller.

Two panel template: left and right

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import tkinter
from dptools.static import styling
from dptools.tkcomponents.baseapp import notebookview


class BasePanelView:
    """
    Root view for disappeer root controller
    """
    def __init__(self, root, title='RootView'):
        # Configure root
        self.root = root
        self.root.minsize(200, 200)
        self.root.title(title)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Run setup
        styling.config_ttk_styling()
        self.root_menubar = self.config_menubar()
        self.main_frame = self.config_main_frame()
        self.main_pane = self.config_main_pane()
        self.left_panel = self.config_panel()
        self.right_panel = self.config_panel()

        # Set focus
        self.root.focus()

    def config_menubar(self):
        """
        Add all styling for the menubar
        """
        root_menubar = tkinter.Menu(self.root, **styling.menu_bar_styling)
        self.root.config(menu=root_menubar)
        return root_menubar

    def add_cascade_to_menubar(self, **kwargs):
        menu = tkinter.Menu(self.root_menubar, **styling.menu_bar_styling)
        self.root_menubar.add_cascade(menu=menu, **kwargs)
        return menu

    def config_main_frame(self):
        """
        Configure the main outer frame for the main view
        """
        main_frame = tkinter.Frame(self.root, background=styling.background_color)
        main_frame.grid(column=0, row=0, sticky=styling.sticky_all)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        return main_frame

    def config_main_pane(self):
        """
        Configure the paned window for main view
        """
        main_pane = tkinter.PanedWindow(self.main_frame, orient="horizontal", sashwidth=10, background='black', borderwidth=0)
        main_pane.grid(row=0, column=0, sticky=styling.sticky_all)
        return main_pane

    def config_panel(self):
        """
        Configure left panel for main pane
        """
        panel = notebookview.RootPanelView(self.main_pane)
        return panel

    def add_tab_to_left_panel(self, *args, **kwargs):
        return self.left_panel.add_tab_to_notebook(*args, **kwargs)

    def add_tab_to_right_panel(self, *args, **kwargs):
        return self.right_panel.add_tab_to_notebook(*args, **kwargs)
