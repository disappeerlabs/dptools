"""
smackserverreceivecommand.py

Partial implementation of command pattern for:
    - receiving results that are put to queue by smack server

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.commands import abstracts


class SmackServerReceiveResult(abstracts.AbstractResult):
    def __init__(self, result):
        super().__init__(result)
