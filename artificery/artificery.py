import json
import glob
import os

class Artificery():
    def __init__(self):
        self.reloat_parsers()

    def parse(self, params_path):
        with open(params_path, 'r') as f:
            params = json.load(f)
        net = self.create_net(params)
        return net

    def create_net(self, params):
        if 'path' in params:
            return parse(params['path'])
        elif 'type' in params:
            net_type = prams['type'].tolower()
            net = self.parsers[net_type](params, create_net=self.create_net)
        else:
            raise Exception("Neither type nor path specified.")

        return net

    def reload_parsers(self):
        paser_template = os.path.join(os.path.dirname(__file__), "parsers/*.py")
        all_paths = glob.glob(parser_template)

        self.parsers = {}
        for parser_path in all_paths:
            parser_full_name = os.path.basename(parser_path)
            parser_name = os.path.splitext(parser_full_name)[0]
            if parser_name.tolower() != parser_name:
                raise Exception("Parser name cannot contain uppercase letters."
                                "Violator: {}".format(parser_path))

            parser  = importlib.import_module("parsers.{}".format(parser_name))
            self.parsers[parser_name] = parser.parse

