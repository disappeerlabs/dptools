# Disappeer Tools

Attempt at a library to store independent, and independently tested 
components, systems and subsystems developed for the Disappeer project.

The goal is a library that has tools and components that can be
imported into any future project.

Examples:

- utlities
    - applogger
    - observable
    - queueconsumer
- subsystems
    - gpg 
    - networking
    - tornet
    - command client/server
 - etc.
 
 To be used as basis for planned DP rebuild. 
 
 # Notes
 
 Add slow flag to run all tests:
 
 `slow=1 python -m unittest gpg/agents/tests/test_decrypter.py -v` 