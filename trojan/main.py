import os
from .connection import connect


REMOTE_PYTHON = os.environ.get('PYTHON_TROJAN_REMOTE', 'python')
BASH_CMD = 'exec {remote} -u $({remote} -u -c "{stage1_text}") clean' + os.linesep
SSH_CMD = "ssh {target_host} 'bash -'"
STAGES_DIR = os.path.join(os.path.dirname(__file__), 'stages')
STAGE1_PATH = os.path.join(STAGES_DIR, 'stage1.py')
STAGE2_PATH = os.path.join(STAGES_DIR, 'stage2.py')


class LineWriter(object):
    def __init__(self, target):
        self.target = target

    def write(self, line):
        self.target.write((line + os.linesep).encode())


def run(target_host, payload, name=None, clean=False):
    """Run provided payload on remote host returning communication
    channel to it.
    """
    p = connect(target_host)
    stdin = LineWriter(p.stdin)

    # locate and read stage1
    with open(STAGE1_PATH) as stage1_file:
        stage1_text = stage1_file.read()

    # start stage1 with bash
    command = BASH_CMD.format(
        remote=REMOTE_PYTHON,
        stage1_text=stage1_text
    )
    stdin.write(command)

    # push stage2 to remote
    with open(STAGE2_PATH) as stage2_file:
        stage2_text = stage2_file.read()
    stdin.write(stage2_text)
    stdin.write('EOF')

    line = p.stdout.readline()
    if line.strip() != 'STAGE2'.encode():
        raise RuntimeError('stage2 startup failed {}'.format(line))

    # rename remote process
    if name is not None:
        stdin.write('NAME:{}'.format(name))
        line = p.stdout.readline()
        if line.strip() != 'STAGE2'.encode():
            raise RuntimeError('stage2 startup failed: {}'.format(line))
    stdin.write('CLEAN')

    # start payload on remote host
    stdin.write('PUT')
    stdin.write(payload)
    stdin.write('EOF')

    return p
