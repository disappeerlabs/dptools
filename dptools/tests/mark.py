"""
mark.py	

Mark individual tests by unpacking tuple and passing it in to test decorator

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import os


slow = (not os.getenv('slow'), 'set slow flag to run')
