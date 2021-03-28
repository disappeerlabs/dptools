"""
basemodel.py

"""


class BaseModel:

    def __init__(self, args=None, root=None, queue=None):
        self.args = args
        self.root = root
        self.queue = queue
    
    def register_widget_model(self, name, val):
        setattr(self, name, val(args=self.args, root=self.root, queue=self.queue))
        return getattr(self, name)
