#!/usr/bin/python3
""" A program that contains the entry point of the command interpreter """

import cmd
from datetime import datetime
from models.base_model import BaseModel
from shlex import split


class HBNBCommand(cmd.Cmd):
    """ the class entry point of the comaand interpreter """

    prompt = '(hbnb) '

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Exits the program at end of file"""
        return True

    def emptyline(self):
        """Does nothing at an empty line"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
