import subprocess

path_to_cwltool = 'cwl-runner'


def call_cwl(task, params):
    subprocess.call([path_to_cwltool, task, params])
