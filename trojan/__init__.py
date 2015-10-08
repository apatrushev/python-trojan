import os
from subprocess import Popen, PIPE


bash_code = '''[ -e {filepath} ] || {{
    # be sure that target dir exists
    mkdir -p "`dirname {filepath}`"
    [ -d "`dirname {filepath}`" ] || {{
        echo 'ERROR:target dir is not a dir'
        pwd
        ls -la
        exit
    }}

    # try to write to target file
    echo '' >{filepath}
    [ $? -eq 0 ] || {{
        echo 'ERROR:can not write to file'
        exit
    }}

    # check python
    which python &>/dev/null
    [ $? -eq 0 ] || {{
        echo 'ERROR:python not found'
        exit
    }}
    echo 'GET'

    # skip echo start
    read LINE

    # write to file until eof
    while read LINE; do
        if [ "$LINE" = "EOF" ]; then
            break;
        fi
        echo "$LINE" >>{filepath}
    done
    echo 'START'
}}
echo 'START'
'''


def run(target_host, module_text, target_path=None, clean=False):
    p = Popen(
        "ssh {} 'bash -'".format(target_host),
        shell=True,
        bufsize=0,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=True
    )

    if target_path is None:
        p.stdin.write('mktemp -u -t trojanXXX.py' + os.linesep)
        target_path = p.stdout.readline().strip()
    elif clean:
        p.stdin.write(
            'rm -f {filepath} &>/dev/null'.format(
                filepath=target_path
            ) + os.linesep
        )

    p.stdin.write(bash_code.format(filepath=target_path))
    answer = p.stdout.readline().strip()

    if answer == 'GET':
        p.stdin.write(module_text)
        p.stdin.write(os.linesep)
        p.stdin.write('EOF' + os.linesep)
        answer = p.stdout.readline().strip()

    if answer == 'START':
        print >>p.stdin, "exec python {filepath}".format(
            filepath=target_path
        )
    else:
        p.stdin.close()
        p.wait()
        raise RuntimeError('Failed to run. Wrong answer: {}'.fromat(answer))

    return p
