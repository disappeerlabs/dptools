# Disappeer Tools

Library for independent and independently tested components, systems 
and subsystems extracted from the Disappeer project.

The goal is a library that has tools and components 
that can be imported into and leveraged by any future project 
such as the Disappeer rebuild. 

## Inventory

- utlities
    - applogger
        ```python 
        # initialize app logger at program launch 
        log = AppLogger(AppLogger.name).create()
        # access app logger in any subsequent module
        import logging
        log = logging.getLogger(AppLogger.name) 
        ```
    - observable
- subsystems
    - gpg 
        - client
        - agents
    - networking
        - torproxy
        - smackprotocol
        - client/server abstracts
    - command abstracts
        - command, handler, result
        - integration with queue consumer
    - tkcomponents
        - queue consumer
        - baseapp
        - debugwidget
        - popuplauncher
            ```python 
            from dptools.tkcomponents.popuplauncher import launch_popup, alertbox
            r = launch_popup(alertbox, tk_root, "is this thing on?")
            ```
    - db interface
 - etc.
 
 
 ## Tests
 
Add slow flag to run all tests:
 
`slow=1 python -m unittest` 
 
