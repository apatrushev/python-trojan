import os
from subprocess import Popen, PIPE


COMMAND = 'bash -l'
SSH_CONFIG = '~/.ssh/config'


def connect(target_host):
    SSH_CMD = 'ssh {target_host} {command}'
    command = SSH_CMD.format(
        target_host=target_host,
        command=COMMAND
    )
    proc = Popen(
        command,
        shell=True,
        bufsize=0,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=True
    )
    return proc


if not os.environ.get('PYTHON_TROJAN_SSH', None):
    try:
        import paramiko
        import threading

        def pipe(source, destination):
            while True:
                source.channel.in_buffer._lock.acquire()
                ready_bytes = 1
                try:
                    ready_bytes = len(source.channel.in_buffer._buffer)
                finally:
                    source.channel.in_buffer._lock.release()
                data = source.read(ready_bytes or 1)
                if not data:
                    return
                destination.write(data)

        def wrap_output(source):
            r, w = os.pipe()
            r, w = os.fdopen(r, 'rb', 0), os.fdopen(w, 'wb', 0)
            thread = threading.Thread(target=pipe, args=(source, w))
            thread.daemon = True
            thread.start()
            return r

        class connect:
            def __init__(self, target_host):
                self.target_host = target_host

                config = paramiko.config.SSHConfig()
                config_path = os.path.expanduser(SSH_CONFIG)
                with open(config_path) as f:
                    config.parse(f)

                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
                self.ssh.connect(config.lookup(self.target_host)['hostname'])
                self.stdin, self.stdout, self.stderr = self.ssh.exec_command(COMMAND)
                self.stdout = wrap_output(self.stdout)
                self.stderr = wrap_output(self.stderr)
    except:
        pass
