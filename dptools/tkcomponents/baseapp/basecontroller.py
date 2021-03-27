"""
basecontroller.py

Base class for app root controller
"""

import logging
from dptools.utilities.applogger import AppLogger
from dptools.tkcomponents.baseapp import basepanelview, queueconsumer, basemodel


class BaseController(queueconsumer.QueueConsumer):

    def __init__(self, args=None, root=None):
        queueconsumer.QueueConsumer.__init__(self, root)
        self.args = args
        self.root = root
        self.root_view = self.set_root_view()
        self.root_model = self.set_root_model()

    def add_widget_left_panel(self, component_package):
        return self.register_widget(component_package, self.root_view.add_tab_to_left_panel, self.root_model.register_widget_model)

    def add_widget_right_panel(self, component_package):
        return self.register_widget(component_package, self.root_view.add_tab_to_right_panel, self.root_model.register_widget_model)

    def register_widget(self, component_package, attach_view_method, attach_model_method):
        return component_package.register_widget(self.root, attach_view_method, attach_model_method)

    def set_root_view(self):
        return basepanelview.BasePanelView(self.root)
    
    def set_root_model(self):
        return basemodel.BaseModel(args=self.args, root=self.root)

    def check_payload(self, payload):
        raise NotImplementedError

    def handle_queue_payload(self, payload):
        raise NotImplementedError

    def handle_queue_payload_error(self, payload):
        raise NotImplementedError