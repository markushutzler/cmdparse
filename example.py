#!/usr/bin/python
# -*- coding: utf-8 -*-

import cmdparse


class TestCommand(cmdparse.Command):
    """Test command class to demonstrate command with extra argument."""

    __desc__ = "A detailed description of test command displayed if -h " + \
               "is set."
    __help__ = "A test command"
    __cmd__ = "test"

    def __init__(self):
        cmdparse.Command.__init__(self)

    def add_arguments(self, parser):
        parser.add_argument('-x', dest='xxx', action='store_true',
                            help="Print 3 times x.")

    def run(self, args):
        print("test command called")
        if args.xxx:
            print("XXX")


class NewCommand(cmdparse.Command):
    """Example command class to demonstrate minimal implementation needed."""
    __help__ = "A new test command"
    __cmd__ = "new"


class EmptyCommand(cmdparse.Command):
    pass

if __name__ == "__main__":
    # Set up parser
    parser = cmdparse.ArgumentParser(description='Test application')

    # Add test commands
    parser.add_command(TestCommand)
    parser.add_command(NewCommand)

    # Test exception (Uncomment lines to test ValueError exceptions.)
    # parser.add_command(EmptyCommand)
    # parser.add_command(NewCommand)

    # Parse arguments
    args = parser.parse_args()

    # Retrieve, initialise and run command class
    cmd_class = args.command
    cmd = cmd_class()
    cmd.run(args)
