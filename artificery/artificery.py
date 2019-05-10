import json
import glob
import os
from importlib import util

def import_file(full_name, path):
    spec = util.spec_from_file_location(full_name, path)
    mod = util.module_from_spec(spec)

    spec.loader.exec_module(mod)
    return mod

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

class Artificery():
    def __init__(self):
        self.reload_parsers()
        self.param_folders = set()

    def parse(self, params_file):
        print (params_file)
        folder = os.path.dirname(params_file)

        if folder != '' and folder not in self.param_folders:
            added_folder = True
            self.param_folders.add(folder)
        else:
            added_folder = False

        if os.path.isfile(params_file):
            with open(params_file, 'r') as f:
                params = json.load(f)
        else:
            global_path = None
            for folder in self.param_folders:
                global_path = find(params_file, folder)
                if global_path is not None:
                    break
            if global_path is not None:
                with open(global_path, 'r') as f:
                    params = json.load(f)
            else:
                raise Exception("Cannot find params file: {}".format(params_file))

        net = self.create_net(params)
        if added_folder:
            self.param_folders.remove(folder)

        return net

    def create_net(self, params):
        if 'path' in params:
            return self.parse(params['path'])

        elif 'type' in params:
            net_type = params['type'].lower()
            net = self.parsers[net_type](params, create_module=self.create_net)
        else:
            raise Exception("Neither type nor path specified.")

        return net

    def reload_parsers(self):
        parser_template = os.path.join(os.path.dirname(__file__), "parsers/*")
        parser_folders = glob.glob(parser_template)

        self.parsers = {}
        for folder in parser_folders:
            parser_path = os.path.join(folder, "parse.py")
            parser_name = folder.split('/')[-1]

            if parser_name.lower() != parser_name:
                raise Exception("Parser name cannot contain uppercase letters."
                                "Violator: {}".format(folder))

            parser  = import_file("parser", parser_path)
            self.parsers[parser_name] = parser.parse


