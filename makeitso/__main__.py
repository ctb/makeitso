#! /usr/bin/env python
import argparse
import requests
import os.path
from .logging import *
import subprocess

path_to_cwltool = 'cwl-runner'


def main():
    set_quiet(False)

    commands = {'run': run }
    parser = argparse.ArgumentParser(
        description='do things with CWL',
        usage='''makeitso <command> [<args>]

Commands can be:

run                    run CWL workflow on current computer

Use '-h' to get subcommand-specific help, e.g.

sourmash compute -h
.
''')
    parser.add_argument('command')
    args = parser.parse_args(sys.argv[1:2])
    if args.command not in commands:
        error('Unrecognized command')
        parser.print_help()
        sys.exit(1)

    cmd = commands.get(args.command)
    cmd(sys.argv[2:])


def run(args):
    p = argparse.ArgumentParser()
    p.add_argument('taskname')
    p.add_argument('params_yaml')
    args = p.parse_args(args)

    if args.taskname.startswith('http'):
        url = args.taskname
    else:
        # try repo/path:tag
        user, path = args.taskname.split('/', 1)

        if '/' in path:
            repo, path = path.split('/', 1)
        else:
            repo = path
            path = ''

        branch = 'master'
        if ':' in path:
            path, branch = path.rsplit(':', 1)

        if path == '':
            path = 'Dockstore.cwl'        # hack

        github_url = 'https://raw.githubusercontent.com/{}/{}/{}/{}'
        url = github_url.format(user, repo, branch, path)

    notify('task: {}'.format(url))
    notify('params: {}'.format(args.params_yaml))

    subprocess.call([path_to_cwltool, url, args.params_yaml])


if __name__ == '__main__':
   main()
