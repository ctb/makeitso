#! /usr/bin/env python
import argparse
import sys
import requests
from requests.auth import HTTPDigestAuth
import json

from .logging import notify, set_quiet
from .find_cwldef import find_cwldef
from .call_cwl import call_cwl
from .server import app


def main():
    set_quiet(False)

    commands = {'run': run, 'server': server, 'sendtask': sendtask}
    parser = argparse.ArgumentParser(
        description='do things with CWL',
        usage='''makeitso <command> [<args>]

Commands can be:

run                    run CWL workflow on current computer
server                 run a task pool server
worker                 run a task pool worker
sendtask               send a task to the server

Use '-h' to get subcommand-specific help, e.g.

makeitso run -h
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

    task = find_cwldef(args.taskname)

    notify('task: {}'.format(task))
    notify('params: {}'.format(args.params_yaml))

    call_cwl(task, args.params_yaml)


def server(args):
    p = argparse.ArgumentParser()
    p.add_argument('-p', '--port', type=int, default=5000)
    args = p.parse_args(args)

    app.run(debug=True, port=args.port)


def sendtask(args):
    p = argparse.ArgumentParser()
    p.add_argument('-S', '--server-url', default='http://localhost:5000')
    p.add_argument('taskname')
    p.add_argument('params')
    args = p.parse_args(args)

    full_url = args.server_url + '/todo/api/v1.0/tasks'

    # load up the payload
    params_content = open(args.params).read()
    taskdict = dict(taskname=args.taskname, params=params_content)

    # authenticate & POST
    auth = HTTPDigestAuth('miguel', 'python')
    response = requests.post(full_url, json=taskdict, auth=auth)

    response.raise_for_status()


if __name__ == '__main__':
   main()
