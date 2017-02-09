from __future__ import print_function
import sys, tempfile, os
import time
fd, path = tempfile.mkstemp(suffix='.py', prefix='trojan_stage2_')
print(path)
def reader():
    while 1: yield sys.stdin.readline()
for line in reader():
    if line.strip() == 'EOF': break
    os.write(fd, line.encode())
