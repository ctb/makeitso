import subprocess
import tempfile

path_to_cwltool = 'cwl-runner'


def save_params(params_str):
    fp = tempfile.NamedTemporaryFile(mode='w', suffix='.makeitso')
    fp.write(params_str)
    fp.close()
    
    return fp.name


def call_cwl(task, params):
    print('*** here I run: {} {} {}'.format(path_to_cwltool, task, params))
    #subprocess.call(['/home/tx160085/env/bin/python', path_to_cwltool, task, params])
