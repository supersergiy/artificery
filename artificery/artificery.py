import json
import glob
import os
from importlib import util
import torch

def import_file(full_name, path):
    spec = util.spec_from_file_location(full_name, path)
    mod = util.module_from_spec(spec)

    spec.loader.exec_module(mod)
    return mod

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def find_file_in_folder_set(filename, folder_set):
    filename = os.path.expanduser(filename)
    found_file = None

    if os.path.isfile(filename):
        found_file = filename
    else:
        global_path = None
        for parent in folder_set:
            global_path = os.path.join(parent, filename)

            if os.path.isfile(global_path):
                found_file = global_path
                break
    return found_file

class Artificery():
    def __init__(self, checkpoint_init=False):
        self.reload_parsers()
        self.param_folders = set()
        self.used_specfiles = []
        self.checkpoint_init = checkpoint_init

    def parse(self, params_file):
        params_file = os.path.expanduser(params_file)
        print (params_file)

        folder = os.path.dirname(params_file)
        if folder != '' and folder not in self.param_folders:
            added_folder = True
            self.param_folders.add(folder)
        else:
            added_folder = False

        found_file = find_file_in_folder_set(params_file, self.param_folders)
        if found_file is None:
            raise Exception("Cannot find params file: {}".format(params_file))

        with open(found_file, 'r') as f:
            params = json.load(f)
        self.used_specfiles.append(found_file)

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

        if self.checkpoint_init and 'checkpoint_init' in params:
            checkpoint_file = params['checkpoint_init']
            found_file = find_file_in_folder_set(checkpoint_file, self.param_folders)
            if found_file is None:
                raise Exception("Cannot find init file: {}".format(checkpoint_file))
            print ("loading weights from {}".format(found_file))
            net.load_state_dict(torch.load(found_file))
            print ("loaded! mean weight [0] == {}".format(torch.mean(list(net.parameters())[0])))
        if 'trainable' in params and params['trainable'] == False:
            print ("Setting layer to non trainable")
            for param in net.parameters():
                param.requires_grad = False
        return net

    def reload_parsers(self):
        parser_template = os.path.join(os.path.dirname(__file__), "parsers/*")
        parser_folders = glob.glob(parser_template)

        self.parsers = {}
        for folder in parser_folders:
            if os.path.isdir(folder):
                parser_path = os.path.join(folder, "parse.py")
                if os.path.isfile(parser_path) :
                    parser_name = folder.split('/')[-1]

                    if parser_name.lower() != parser_name:
                        raise Exception("Parser name cannot contain uppercase letters."
                                        "Violator: {}".format(folder))

                    parser  = import_file("parser", parser_path)
                    self.parsers[parser_name] = parser.parse


