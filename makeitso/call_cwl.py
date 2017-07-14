import subprocess
import tempfile

from . import config


def save_params(params_str):
    fp = tempfile.NamedTemporaryFile(mode='w', suffix='.makeitso')
    fp.write(params_str)
    fp.close()
    
    return fp.name


def call_cwl(task, params):
    print('*** attempting to run {} {}'.format(task, params))

    call_list = list(config.process_call)
    call_list += [task, params]
    subprocess.call(call_list)
