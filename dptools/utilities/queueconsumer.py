"""
queueconsumer.py

Module for QueueConsumer controller base class.

Child classes must implement:
    - log attribute

Child classes should implement:
    - handle_queue_payload
    - handle_queue_payload_error

Queue Consumer presumes that queue payloads are:
    - dictionaries
    - dictionary has key for 'desc'
    - TODO: Determine if payload should be its own object
        - e.g. class of type ConsumablePayload

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import queue


class QueueConsumer:

    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.poll_queue()

    def poll_queue(self):
        self.consume_queue()
        self.root.after(200, self.poll_queue)

    def consume_queue(self):
        if not self.queue.empty():
            got = self.queue.get()
            self.process_queue_result(got)
            self.queue.task_done()

    def process_queue_result(self, payload):
        check = self.check_payload(payload)
        if check:
            self.handle_queue_payload(payload)
        else:
            self.handle_queue_payload_error(payload)

    def check_payload(self, payload):
        if not isinstance(payload, dict):
            self.log.error("{}-QueueConsumer payload of type {} is not dict: {}".format(type(self).__name__, type(payload), payload))
            return False
        try:
            desc = payload['desc']
        except KeyError as err:
            self.log.error("{}-QueueConsumer, malformed payload: {}, {}".format(type(self).__name__, err, payload))
            return False
        return payload

    def handle_queue_payload(self, payload):
        raise NotImplementedError

    def handle_queue_payload_error(self, payload):
        raise NotImplementedError
