"""
debugframe.py	

Basic debug frame widget with text box and buttons

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from dptools.static import styling


class DebugFrame(tkinter.Frame):

    def __init__(self, parent):
        super().__init__(parent, background=styling.background_color, padx=10, pady=10)
        self.parent = parent
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)

        self.debug_text_box = self.config_text_box()
        self.debug_button_1 = self.config_button_1()
        self.debug_button_2 = self.config_button_2()

    def config_button_1(self):
        debug_button = ttk.Button(self, text="Debug One")
        debug_button.grid(row=1, column=0, sticky=styling.sticky_ew, padx=(5, 0), pady=(10, 5))
        return debug_button

    def config_button_2(self):
        debug_button_2 = ttk.Button(self, text="Debug Two")
        debug_button_2.grid(row=2, column=0, sticky=styling.sticky_ew, padx=(5, 0), pady=(10, 5))
        return debug_button_2

    def config_text_box(self):
        debug_text_box = tkinter.Text(self, **styling.debug_text_area)
        debug_text_box.grid(row=0, column=0, sticky=styling.sticky_all)
        return debug_text_box

    def print_to_debug(self, msg):
        """
        Clear debug text box and insert msg.
        """
        self.debug_text_box.delete('1.0', 'end')
        self.debug_text_box.insert('1.0', msg + "\n")

    def append_to_debug(self, msg):
        """
        Append msg to end of debug text box. Scroll to end of textbox.
        """
        self.debug_text_box.insert('end', msg + "\n")
        self.debug_text_box.see('end')

    def config_event_bindings(self, debug_button_1_action, debug_button_2_action):
        self.debug_button_1.bind("<ButtonRelease-1>", debug_button_1_action)
        self.debug_button_2.bind("<ButtonRelease-1>", debug_button_2_action)
