"""
__init__.py	

> ENTER DESCRIPTION HERE

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""


def launch_popup(popup_widget, *args):
    window = popup_widget.initialize(*args)
    result = window.show()
    return result
