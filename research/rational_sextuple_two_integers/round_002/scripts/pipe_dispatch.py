"""Use the CLI's documented stdin prompt mode; preserve all native input bytes."""
from pathlib import Path
import runpy
import subprocess

_original_run = subprocess.run

def run_with_stdin(args, *positional, **kwargs):
    if isinstance(args, (list, tuple)) and args and args[0] == 'copilot' and '-p' in args:
        args = list(args)
        index = args.index('-p')
        prompt = args[index + 1]
        del args[index:index + 2]
        if 'input' in kwargs or 'stdin' in kwargs:
            raise ValueError('Ambiguous prompt transport')
        kwargs['input'] = prompt.encode('utf-8')
    return _original_run(args, *positional, **kwargs)

if __name__ == '__main__':
    subprocess.run = run_with_stdin
    runpy.run_path(str(Path(__file__).with_name('launch_dispatch.py')), run_name='__main__')
