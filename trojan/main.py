import os
from subprocess import Popen, PIPE


BASH_CMD = 'exec python -u $(python -u -c "{stage1_text}") clean' + os.linesep
SSH_CMD = "ssh {target_host} 'bash -'"
STAGES_DIR = os.path.join(os.path.dirname(__file__), 'stages')
STAGE1_PATH = os.path.join(STAGES_DIR, 'stage1.py')
STAGE2_PATH = os.path.join(STAGES_DIR, 'stage2.py')


def run(target_host, payload, name=None, clean=False):
    """Run provided payload on remote host returning communication
    channel to it.
    """
    p = Popen(
        SSH_CMD.format(target_host=target_host),
        shell=True,
        bufsize=0,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=True
    )

    # locate and read stage1
    with open(STAGE1_PATH) as stage1_file:
        stage1_text = stage1_file.read()

    # start stage1 with bash
    p.stdin.write(BASH_CMD.format(stage1_text=stage1_text))

    # push stage2 to remote
    with open(STAGE2_PATH) as stage2_file:
        stage2_text = stage2_file.read()
    p.stdin.write(stage2_text + os.linesep)
    p.stdin.write('EOF' + os.linesep)

    # rename remote process
    if name is not None:
        p.stdin.write('NAME:{}'.format(name) + os.linesep)
    p.stdin.write('CLEAN' + os.linesep)

    # start payload on remote host
    p.stdin.write('PUT' + os.linesep)
    p.stdin.write(payload + os.linesep)
    p.stdin.write('EOF' + os.linesep)

    return p
