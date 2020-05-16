"""
queuetoyappcontroller.py	

Queue Consumer instance of toy app controller

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from dptools.utilities import queueconsumer
from dptools.utilities.applogger import method_log
from dptools.tkcomponents.toyapp.controllers import basecontroller


class QueueToyAppController(basecontroller.BaseController, queueconsumer.QueueConsumer):

    def __init__(self, root):
        super().__init__(root)
        self.debug_widget.click_debug_2_override(self.override)

    def override(self, event):
        print("THIS IS THE OVERRIDE!!!!!")
        payload = dict(desc='test queue put', msg="THIS IS A MESSAGE TO THE QUEUE")
        self.queue.put(payload)

    @method_log()
    def handle_queue_payload(self, payload):
        self.log.debug("Received queue payload: " + str(payload))

    def handle_queue_payload_error(self, payload):
        self.log.debug("Received queue payload ERROR: " + str(payload))
