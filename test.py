import sys
import select
import click
import trojan


MODULE_TEXT = '''import sys
import subprocess
for l in sys.stdin.readline():
    subprocess.call(l, shell=True)
'''


@click.command()
@click.argument('host')
def main(host):
    p = trojan.run(host, MODULE_TEXT, clean=True)
    handles = [
        sys.stdin.fileno(),
        p.stdout.fileno(),
        p.stderr.fileno()
    ]
    while True:
        rd, wr, xl = select.select(handles, [], [])
        if sys.stdin.fileno() in rd:
            cmd = sys.stdin.readline()
            if len(cmd) == 0:
                break
            p.stdin.write(cmd)
        if p.stdout.fileno() in rd:
            sys.stdout.write(p.stdout.read(1000))
        if p.stderr.fileno() in rd:
            sys.stderr.write(p.stderr.read(1000))

main()
