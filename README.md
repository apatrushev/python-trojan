# python-trojan
Small library to execute some python code remotely.

Library use ssh connection to bootstrap remote python process.

shell.py is the example of module code that can be run remotely.

## Notes on
You can not use just python for this task because if you will
provide module through python's stdin you will lose communication
channel with remote process (python starts to interpret module
only after stdin close).

So trojan module use some bash bootstrapping code to get rid of
that problem.

Two stage bootstrapping is used to reduce the number of problems
with escaping character's in the initial bash code.
