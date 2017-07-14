#! /usr/bin/env python
import argparse

from .logging import *
from .find_cwldef import find_cwldef
from .call_cwl import call_cwl


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

    task = find_cwldef(args.taskname)

    notify('task: {}'.format(task))
    notify('params: {}'.format(args.params_yaml))

    call_cwl(task, args.params_yaml)


if __name__ == '__main__':
   main()
