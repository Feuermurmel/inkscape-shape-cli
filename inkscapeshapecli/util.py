import contextlib
import os
import subprocess


class UserError(Exception):
    def __init__(self, message, *args):
        super(UserError, self).__init__(message.format(*args))


@contextlib.contextmanager
def command_context(args, remove_env=[], set_env={}, working_dir=None, use_stderr=False):
    env = dict(os.environ)

    for i in remove_env:
        del env[i]

    for k, v in set_env.items():
        env[k] = v

    if use_stderr:
        stderr = subprocess.PIPE
    else:
        stderr = None

    try:
        process = subprocess.Popen(args, env=env, cwd=working_dir, stderr=stderr)
    except OSError as e:
        raise UserError('Error running {}: {}', args[0], e)

    try:
        yield process
    except BaseException:
        process.kill()
    finally:
        # Use communicate so that we won't deadlock if the process generates
        # some unread output.
        process.communicate()

    if process.returncode:
        raise UserError('Command failed: {}', ' '.join(args))


def command(args, remove_env=[], set_env={}, working_dir=None):
    with command_context(args, remove_env, set_env, working_dir):
        pass
