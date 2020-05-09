"""
observable.py

A simple observable class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


class Observable:

    def __init__(self, data=None):
        self.data = data
        self.callbacks = {}
        self.observer_list = []
        # self.add_callback(self.update_observers)

    def get(self):
        return self.data

    def set(self, data):
        self.data = data
        self.run_callbacks()
        self.update_observers()

    def unset(self):
        self.data = None

    ##############################
    #  CALLBACK METHODS          #
    ##############################

    def add_callback(self, func):
        self.callbacks[func] = 1

    def run_callbacks(self):
        for func in self.callbacks:
            func(self.get())

    def delete_callback(self, func):
        del self.callbacks[func]

    ##############################
    #  OBSERVER METHODS          #
    ##############################

    def update_widget(self, widget_var):
        widget_var.set(self.get())

    def add_observer(self, observer):
        # Todo: address logic issue
        observer.set(self.get())  # New logic added
        self.observer_list.append(observer)
        # self.set(self.data) # Old logic to remove?

    def update_observers(self):
        for item in self.observer_list:
            self.update_widget(item)


if __name__ == '__main__':

    # Some exploratory docs . . .

    # An example callback
    def print_obs_msg(obs_obj):
        print(obs_obj.get())

    # Initialize an observable object and add a callback
    o1 = Observable()
    o1.set("helllo world 0")  # This does not get printed
    o1.add_callback(print_obs_msg)
    # When we update the observable the callback is fired
    o1.set("helllo world 1")  # This prints to stdout, when func is called

    # Above, the callback gets called as a func with the observable itself as its arg

    # Observables are also observers
    o2 = Observable()
    o1.add_observer(o2)

    # TODO: address logic issue
    # When you add an observer, the observable is reset
    # The above prints out the msg again because .set() is called tautologically
    # and all callbacks are run.
    # We don't need to run set for everyone
    # When we update_observers, we call set on the observer with the output of self.get().
    # Perhaps we only need to call set on the new observer
    assert o2.get() == o1.get()
    o1.set("hello world 2")
    assert o2.get() == o1.get()

    # We set observers with the value of get
    # When we update observer, we call observer's set method with value of get
    # When we run callbacks, we call the func and pass in self as its arg
    # Should we be passing in .get() instead of self?

