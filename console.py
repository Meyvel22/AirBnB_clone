#!/usr/bin/python3
""" A program that contains the entry point of the command interpreter """

import cmd
from datetime import datetime
from models.base_model import BaseModel
from shlex import split
from models.engine.file_storage import FileStorage

storage = FileStorage()


class HBNBCommand(cmd.Cmd):
    """ the class entry point of the comaand interpreter """

    __class_names = ["BaseModel"]
    prompt = '(hbnb) '

    def do_quit(self, line):
        """Quit command to exit the program"""
        raise SystemExit

    def do_EOF(self, line):
        """Exits the program at end of file"""
        raise SystemExit

    def emptyline(self):
        """Does nothing at an empty line"""
        pass

    def do_create(self, args):
        args_list = args.split(" ")
        if not args:
            print("** class name missing **")
        elif not args_list[0] in HBNBCommand.__class_names:
            print("** class doesn't exist **")
        else:
            print('creating BaseModel instance')
            model = BaseModel()
            storage.new(model)
            storage.save()
            print(model.id)

    def do_create(self, args):
        args_list = args.split(" ")
        if not args:
            print("** class name missing **")
        elif not args_list[0] in HBNBCommand.__class_names:
            print("** class doesn't exist **")
        else:
            print('creating BaseModel instance')
            model = BaseModel()
            storage.new(model)
            storage.save()
            print(model.id)

    def do_show(self, args):
        """
        Prints the string representation of an instance based on the
        class name and id
        """
        args_list = args.split(" ")
        if not args:
            print("** class name missing **")
        elif not args_list[0] in HBNBCommand.__class_names:
            print("** class doesn't exist **")
        elif len(args_list) < 2:
            print("** instance id missing **")
        else:
            class_name, object_id = args_list
            payload = storage.all().get(".".join(args_list))

            if not payload:
                print("** no instance found **")
            else:
                model = BaseModel(payload)
                print(model)

    def do_destroy(self, args):
        """
        Deletes an instance based on the class name and id
        """
        args_list = args.split(" ")
        if not args:
            print("** class name missing **")
        elif not args_list[0] in HBNBCommand.__class_names:
            print("** class doesn't exist **")
        elif len(args_list) < 2:
            print("** instance id missing **")
        else:
            class_name, object_id = args_list
            _id = "{}.{}".format(class_name, object_id)
            data_read = storage.all()
            payload = data_read.get(_id)

            if not payload:
                return print("** no instance found **")

            del data_read[_id]
            storage.update(data_read)
            storage.save()

    def do_all(self, args):
        """
        Prints all string representation of all instances based or
        not on the class name
        """
        args_list = args.split(" ")

        if len(args_list) >= 1 and args_list[0] not in \
                HBNBCommand.__class_names:
            return print("** class doesn't exist **")

        data_read = storage.all()
        if not data_read:
            return

        for key, item in list(data_read.items()):
            print(BaseModel(item))

    # def do_update(self, args):
    #     """
    #     Updates an instance based on the class name and id by adding or
    #     updating attribute
    #     """
    #     args_list = args.split(" ")
    #     if not args:
    #         print("** class name missing **")
    #     elif not args_list[0] in HBNBCommand.__class_names:
    #         print("** class doesn't exist **")
    #     elif len(args_list) < 2:
    #         print("** instance id missing **")
    #     else:
    #         _id = "{}.{}".format(args_list[0], args_list[1])
    #         data_read = storage.all()
    #         payload = data_read.get(_id)
    #         if not payload:
    #            return print("** no instance found **")
    #         elif len(args_list) < 3:
    #             return print("** attribute name missing **")
    #         elif len(args_list) < 4:
    #             return print("** value missing **")

    #         attribute = args_list[2]
    #         value = args_list[3]
    #         model = BaseModel(payload)
    #         model.__getattr__(attribute, value, value)
    #         data_read[_id] = payload
    #         storage.update(data_read)
    #         print(payload)
    #         storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
