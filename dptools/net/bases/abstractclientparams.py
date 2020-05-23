"""
abstractclientparams.py	

Data Class to Encapsulate Params for Abstract Client Class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import queue
from dataclasses import dataclass


@dataclass
class AbstractClientParams:
    host: str
    port: int
    command: str
    nonce: str
    payload_dict: dict
    queue: queue.Queue
