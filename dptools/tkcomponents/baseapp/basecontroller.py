"""
basecontroller.py

Base class for app root controller
"""

import logging
from dptools.utilities.applogger import AppLogger
from dptools.utilities import queueconsumer
from dptools.tkcomponents.baseapp import basepanelview


class BaseController(queueconsumer.QueueConsumer):

    def __init__(self, root):
        queueconsumer.QueueConsumer.__init__(self, root)
        self.root = root
        self.root_view = basepanelview.BasePanelView(self.root)
        self.log = logging.getLogger(AppLogger.name)

    def add_widget_left_panel(self, component_package):
        output = component_package.register_widget(self.root, self.root_view.add_tab_to_left_panel)
        return output

    def add_widget_right_panel(self, component_package):
        output = component_package.register_widget(self.root, self.root_view.add_tab_to_right_panel)
        return output

    def handle_queue_payload(self, payload):
        self.log.debug("Received queue payload: " + str(payload))

    def handle_queue_payload_error(self, payload):
        self.log.debug("Received queue payload ERROR: " + str(payload))
