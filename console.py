#!/usr/bin/python3
""" A program that contains the entry point of the command interpreter """

import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """ the class entry point of the comaand interpreter """
    prompt = "(hbnb) "

    model_list = ['BaseModel', 'User', 'State',
                  'City', 'Amenity', "Place", "Review"]
    queries = ['all', 'count', 'show', 'destroy', 'update']

    def precmd(self, line):
        """When precmd() is called, the 'line' is stripped of [, . ()"] then
        joined and passed to the interpreter"""
        if "." in line:
            line_arg = line.replace('.', ' ').replace(',', ' ')\
                .replace('(', ' ').replace('"', '').replace(')', ' ')
            line_arg = line_arg.split()
            line_arg[0], line_arg[1] = line_arg[1], line_arg[0]
            line = " ".join(line_arg)
        return cmd.Cmd().precmd(line)

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """Exits the program at end of file"""

        return True

    def emptyline(self):
        """Does nothing at an empty line"""
        return False

    def onecmd(self, args: str):
        pattern = re.compile(
            r"(\w+)\.(\w+)\(((\"[\w|-]+\"),?\s?(\"\w+\")?,?\s?(\"?\w+\"?)?)?\)"
        )
        match = re.search(pattern, args)
        if match:
            self.handle_match(match)
        elif args == "quit":
            return self.do_quit(args)
        elif args == "EOF":
            return self.do_EOF(args)
        else:
            cmd.Cmd.onecmd(self, args)

    @classmethod
    def handle_errors(cls, args, **kwargs):
        if "all" in kwargs.values():
            if not args:
                return False

        if not args:
            print("** class name missing **")
            return True
        else:
            args = args.split(" ")   # args becomes a list

        n = len(args)

        if args[0] not in HBNBCommand.model_list:
            print("** class doesn't exist **")
            return True

        if 'com' not in kwargs:
            return False

        for arg in kwargs.values():
            if arg in ["show", "destroy", "update"]:
                if n < 2:
                    print("** instance id missing **")
                    return True

            if arg == "update":
                if n < 2:
                    print("** instance id missing **")
                    return True

                elif n < 3:
                    print("** attribute name missing **")
                    return True

                elif n < 4:
                    print("** value missing **")
                    return True

        return False

    def do_create(self, args):
        """Creates a new instance of BaseModel, saves it and prints the id"""

        error = HBNBCommand.handle_errors(args)

        if error:
            return

        obj = eval(args)()
        obj.save()
        print(obj.id)

    def do_show(self, args):
        """
        Prints the string representation of an instance based on the
        class name and id
        """
        error = HBNBCommand.handle_errors(args, com="show")

        if error:
            return

        args = args.split(" ")

        objects = storage.all()
        key = ".".join(args)
        obj = objects.get(key)
        if obj:
            print(obj)
        else:
            print("** no instance found **")

    def do_destroy(self, args: str):
        """
        Deletes an instance based on the class name and id
        """
        error = HBNBCommand.handle_errors(args, com="destroy")

        if error:
            return

        args = args.split(" ")
        objects = models.storage.all()
        key = ".".join(args)

        delete = False
        if key in objects and models.storage.delete(objects[key]):
            pass
        else:
            print("** no instance found **")

    def do_all(self, args):
        """
        Prints all string representation of all instances based or
        not on the class name
        """
        error = HBNBCommand.handle_errors(args, com="all")

        if error:
            return

        args = args.split(" ")

        objects = storage.all()

        if args[0] == "":
            for obj in objects.values():
                print(obj)

        else:
            for key in objects:
                k = key.split(".")
                if k[0] == args[0]:
                    print(objects[key])

    def do_count(self, line):
        """ counts the number of instances of the class passed: 'line'"""
        arg = line.split(" ")
        store = storage.all()
        count = 0

        if len(arg) > 0 and arg[0] not in HBNBCommand.model_list:
            print("** class doesn't exist **")
        else:
            key = arg[0]
            for item in store:
                if key in item:
                    count += 1
            print(count)

    def do_update(self, args):
        """
           Updates an instance based on the class name and id by adding or
           updating attribute
         """
        error = HBNBCommand.handle_errors(args, com="update")

        if error:
            return

        args = args.split()
        class_name = args[0]
        id = args[1]
        attr_name = args[2]
        attr_value = args[3]

        if "\"" in attr_value:
            attr_value = attr_value[1:-1]

        if attr_value.isdigit():
            attr_value = int(attr_value)

        objects = storage.all()
        key = f"{class_name}.{id}"

        for k in objects:   # obj is pointing to the key
            if k == key:
                obj = objects[k]
                setattr(obj, attr_name, attr_value)
                # obj.__setattr(attr_name, attr_value)
                obj.save()
                return

        print("** instance id not found **")

    def handle_match(self, match: re.Match):
        groups = match.groups()
        if groups[0] not in HBNBCommand.model_list:
            print("** class doesn't exist **")
            return
        if groups[1] not in HBNBCommand.queries:
            print(f"** unknown query: '{groups[1]}'")
            return
        if groups[1] == 'all':
            args = f"{groups[1]} {groups[0]}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == 'count':
            args = f"{groups[1]} {groups[0]}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == 'show':
            if groups[3]:
                id = groups[3][1:-1]
            else:
                id =""
            args = f"{groups[1]} {groups[0]} {id}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == "destroy":
            if groups[3]:
                id = groups[3][1:-1]
            else:
                id =""
            args = f"{groups[1]} {groups[0]} {id}"
            cmd.Cmd.onecmd(self, args)
            return
        elif groups[1] == 'update':
            if groups[3] and groups[4]:
                id = groups[3][1:-1]
                attr_name = groups[4][1:-1]
            else:
                id = ""
                attr_name = ""
            if "\"" not in groups[5]:
                attr_value = groups[5]
            elif groups[5]:
                attr_value = groups[5][1:-1]
            else:
                attr_value = ""
            args = f"{groups[1]} {groups[0]} {id} {attr_name} {attr_value}"
            cmd.Cmd.onecmd(self, args)
            return


if __name__ == "__main__":
    HBNBCommand().cmdloop()
