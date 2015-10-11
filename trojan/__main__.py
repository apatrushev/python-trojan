import click
import trojan
import sys
import select


@click.command()
@click.argument('host')
@click.argument('module', type=click.File('rb'))
def main(host, module):
    module_text = module.read()

    p = trojan.run(
        host,
        module_text,
        name=module.name,
        clean=True
    )

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
            line = p.stdout.readline()
            if line:
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                handles.remove(p.stdout.fileno())
                if len(handles) < 2:
                    break
        if p.stderr.fileno() in rd:
            line = p.stderr.readline()
            if line:
                sys.stderr.write(line)
                sys.stderr.flush()
            else:
                handles.remove(p.stderr.fileno())
                if len(handles) < 2:
                    break

main()
