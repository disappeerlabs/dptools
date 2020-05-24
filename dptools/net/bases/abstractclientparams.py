"""
abstractclientparams.py	

Data Class to Encapsulate Params for Abstract Client Class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dataclasses import dataclass


@dataclass
class AbstractClientParams:
    host: str
    port: int
    command: str
    payload_dict: dict
