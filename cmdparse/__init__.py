# -*- coding: utf-8 -*-

# Copyright (c) 2016, Markus Hutzler
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import argparse

__version__ = '0.1'


class Command(object):
    """Argument Parser Command class."""
    __desc__ = ""
    __help__ = ""
    __cmd__ = None

    def __init__(self):
        self._parser = None

    @classmethod
    def _add_arguments_cls(cls, parser):
        self = cls.__new__(cls)
        self.add_arguments(parser)

    def add_arguments(self, parser):
        """Add extra command specific arguments.

        Args:
            parser (`argparse.ArgumentParser`): Parser to manipulate"""
        pass

    def run(self, args):
        """Run the actual command.

        Args:
            args (`Namespace`): Result of parse_args()"""
        pass


class Command2Arg(object):
    """Wrapper class to allow commands to be displayed as arguments."""
    def __init__(self, cmd):
        self.dest = ""
        self.option_strings = []
        self.metavar = cmd.__cmd__
        self.help = cmd.__help__


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser subclass."""

    def __init__(self, *a, **k):
        argparse.ArgumentParser.__init__(self, *a, **k)
        self.commands = []
        self.selected_command = None
        self.selected_command_key = None

    def format_usage(self):
        """Overwrites original format_usage and injects the command."""
        prog = self.prog
        if self.selected_command_key:
            self.prog = prog + " " + self.selected_command_key
        usage = super(ArgumentParser, self).format_usage()
        self.prog = prog
        return usage

    def format_help(self, show_cmd=False):
        """Overwrites format_help. (Adds selected command info)

        Args:
            show_cmd (`bool`): Add list of commands to help message."""
        description = self.description
        self.description = "{% usage-replace %}"
        prog = self.prog
        if self.selected_command_key:
            self.prog = prog + " " + self.selected_command_key
        text = super(ArgumentParser, self).format_help()
        self.prog = prog
        self.description = description

        formatter = self._get_formatter()
        formatter.add_text(self.description)
        if self.selected_command:
            formatter.add_text(self.selected_command.__help__)
            formatter.add_text(self.selected_command.__desc__)
        insertion = formatter.format_help().strip()
        text = text.replace("{% usage-replace %}", insertion)

        if show_cmd:
            formatter = self._get_formatter()
            formatter.start_section("commands")
            for command in self.commands:
                formatter.add_argument(Command2Arg(command))
            formatter.end_section()
            text += "\n" + formatter.format_help()
        return text

    def error_command(self, message):
        """Prints error message for command related errors and exits.

        Args:
            message (`string`): Error message."""
        usage = self.format_usage()
        usage += "%s: error: %s\n" % (self.prog, message)
        usage += "See '%s -h\n" % (self.prog)
        sys.stderr.write(usage)
        sys.exit(2)

    def add_argument(self, *args, **kwargs):
        """Check for command as parameter or destination."""
        dest = kwargs.get("dest", None)
        if dest == "command":
            raise ValueError("command can't be used as destination")
        if not dest and "--command" in args:
            raise ValueError("--command can not be used as parameter")

        return argparse.ArgumentParser.add_argument(self, *args, **kwargs)

    def parse_args(self, args=None, namespace=None):
        """Overwrites original args. (Adds the command to the namespace)"""
        if not self.commands:
            return argparse.ArgumentParser.parse_args(self, args=args,
                                                      namespace=namespace)
        cmd = None
        if args is None:
            args = sys.argv[1:]

        try:
            cmd_key = args.pop(0)
        except IndexError:
            self.error_command("command missing")

        # The only option without command is -h
        if cmd_key == "-h":
            usage = self.format_help(show_cmd=True)
            self._print_message(usage)
            exit()

        for command in self.commands:
            if command.__cmd__ == cmd_key:
                cmd = command
                break

        if not cmd:
            self.error_command("command '%s': unknown" % cmd_key)
        self.selected_command_key = cmd.__cmd__
        self.selected_command = cmd

        # Add command specific arguments

        cmd._add_arguments_cls(self)

        args = argparse.ArgumentParser.parse_args(self, args=args,
                                                  namespace=namespace)
        setattr(args, "command", cmd)
        return args

    def add_command(self, command_class):
        """Add command class to parser.

        Args:
            command_class (`Command`): Command class."""
        if not command_class.__cmd__:
            raise ValueError("Command does not specify command name.")

        if not command_class.__help__:
            raise ValueError("Command does not specify command help.")

        for cmd in self.commands:
            if cmd.__cmd__ == command_class.__cmd__:
                raise ValueError("Duplicate command name added.")

        self.commands.append(command_class)
