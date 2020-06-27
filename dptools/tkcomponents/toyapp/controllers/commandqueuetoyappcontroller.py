"""
commandqueuetoyappcontroller.py	

Controller for demonstration of Command Integration with Queue Consumer Controller

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""
import dptools.commands.checksanity.checksanitycommand
from dptools.tkcomponents.toyapp import toyapp
from dptools.tkcomponents.baseapp import queueconsumer
from dptools.tkcomponents.toyapp.controllers import basecontroller
from dptools.commands import checksanity


class CustomQueueToyAppController(basecontroller.BaseController, queueconsumer.QueueConsumer):

    def __init__(self, root):
        super().__init__(root)
        self.debug_widget.click_debug_1_override(self.button_1_override)
        self.debug_widget.click_debug_2_override(self.button_2_override)

        self.payload_map = dict()
        self.payload_map.update(checksanity.register(self.create_new_key_result))

    def check_payload(self, payload):
        # TODO: remove this override, reimplement the QueueConsumer check to remove restriction to only dicts
        return payload

    def create_new_key_result(self, result_obj):
        self.log.debug("Create new key result method")
        # Unpacking the result means that any dict that gets sent here will cause error out
        self.debug_widget.append_to_textbox(result_obj.result)

    def button_1_override(self, event):
        print("Button 1 override.")
        command = dptools.commands.checksanity.checksanitycommand.CheckSanityCommand("This is the Check Sanity Command")
        self.queue.put(command)

    def button_2_override(self, event):
        print("Button 2 override")
        payload = dict(desc='test queue put', msg="THIS IS A MESSAGE TO THE QUEUE")
        # Putting a dict to the queue to test original functionality
        self.queue.put(payload)

    def handle_queue_payload(self, payload_obj):
        self.log.debug("Received queue payload: " + str(type(payload_obj)))

        target_to_run = self.payload_map[payload_obj.__class__.__name__]
        current_handler = target_to_run(self.queue)
        self.log.debug("Running handler")
        current_handler.handle(payload_obj)

    def handle_queue_payload_error(self, payload):
        self.log.debug("Received queue payload ERROR: " + str(payload))


if __name__ == '__main__':
    app = toyapp.ToyApp(CustomQueueToyAppController)
    app.run()

