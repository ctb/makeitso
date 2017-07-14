#! /usr/bin/env python
from __future__ import print_function
import argparse
import sys
import requests
from requests.auth import HTTPDigestAuth
import json
import time

from .logging import notify, set_quiet
from .find_cwldef import find_cwldef
from .call_cwl import call_cwl, save_params
from .server import app
from . import config


def main():
    set_quiet(False)

    commands = {'run': run, 'server': server, 'sendtask': sendtask,
                'worker': worker}
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
    p.add_argument('--host', default='0.0.0.0')
    args = p.parse_args(args)

    app.run(debug=True, port=args.port, host=args.host)


def sendtask(args):
    p = argparse.ArgumentParser()
    p.add_argument('-S', '--server-url', default=config.default_server_url)
    p.add_argument('taskname')
    p.add_argument('params')
    args = p.parse_args(args)

    notify('using server URL: {}'.format(args.server_url))

    full_url = args.server_url + '/todo/api/v1.0/tasks'

    # load up the payload
    params_content = open(args.params).read()
    taskdict = dict(taskname=args.taskname, params=params_content)

    # authenticate & POST
    auth = HTTPDigestAuth('miguel', 'python')
    response = requests.post(full_url, json=taskdict, auth=auth)

    response.raise_for_status()


def worker(args):
    p = argparse.ArgumentParser()
    p.add_argument('-S', '--server-url', default=config.default_server_url)
    p.add_argument('--quit', action='store_true')
    p.add_argument('--sleep-time', default=1)
    args = p.parse_args(args)

    notify('using server URL: {}'.format(args.server_url))

    full_url = args.server_url + '/todo/api/v1.0/take_task'

    sleep_n = 0
    while 1:
        # authenticate & POST
        auth = HTTPDigestAuth('miguel', 'python')
        response = requests.post(full_url, auth=auth)

        response.raise_for_status()

        result = response.json()
        task = result['task']
        if not task:
            if args.quit:
                print('no more tasks and --quit set; exiting')
                break
            else:
                sleep_n += 1
                print('\rno more tasks; sleeping for a bit. {}'.format(sleep_n), end='')
                sys.stdout.flush()
                try:
                    time.sleep(args.sleep_time)
                except KeyboardInterrupt:
                    print('')
                    break
                continue

        print(task['uri'], task['taskname'])
        print('resolving task "{}"'.format(task['taskname']))
        full_task = find_cwldef(task['taskname'])
        print('...resolved to {}'.format(full_task))

        print('saving params')
        params_filename = save_params(task['params'])
        print('...saved to {}'.format(params_filename))

        call_cwl(full_task, params_filename)

    print('done processing')



if __name__ == '__main__':
   main()
