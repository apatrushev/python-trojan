from __future__ import print_function
import sys
import tempfile
import os


def reader():
    while 1:
        yield sys.stdin.readline()


fd, path = tempfile.mkstemp(suffix='.py', prefix='trojan_stage2_')
print(path)
for line in reader():
    if line.strip() == 'EOF':
        break
    os.write(fd, line.encode())
