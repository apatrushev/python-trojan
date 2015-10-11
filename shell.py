import sys
import subprocess
while True:
    cmd = sys.stdin.readline()
    if not cmd:
        break
    subprocess.call(cmd, shell=True)
