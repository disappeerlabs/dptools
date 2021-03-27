"""
basemodel.py

"""


class BaseModel:

    def __init__(self, args=None, root=None):
        self.args = args
        self.root = root
    
    def register_widget_model(self, name, val):
        setattr(self, name, val(args=self.args, root=self.root))
        return getattr(self, name)
