"""
scratch.py	

Scratch file for disappeer tools work

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""


from dptools.utilities.observable import Observable


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
# print(o2.get())

# We set observers with the value of get
# When we update observer, we call observer's set method with value of get
# When we run callbacks, we call the func and pass in self as its arg
# Should we be passing in .get() instead of self?
