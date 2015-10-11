import sys
import subprocess


def main():
    while True:
        cmd = sys.stdin.readline()
        if not cmd:
            break
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    main()
