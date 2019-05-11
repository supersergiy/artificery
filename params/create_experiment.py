import argparse
import os

from creator import create_param_files, get_setting_filename

def pyr_filename_converter(setting):
    return get_setting_filename('pyramid_categorical', setting,
            custom_folder="~/artificery/params/")

def get_constant_datapath(datapath):
    def constant_datapath(setting):
        return datapath

    return constant_datapath

def main():
    parser = argparse.ArgumentParser()
    args_list = ['compch', 'outch', 'grid', 'step', 'maxvalue', 'trainst']
    for a in args_list:
        parser.add_argument("--{}".format(a), type=str, nargs='+', required=True)

    parser.add_argument("--datapath", type=str, required=True)
    parser.add_argument("--name_flag", type=str, default=None, required=False)

    args = vars(parser.parse_args())
    datapath = args['datapath']
    del args['datapath']
    name_flag = args['name_flag']
    del args['name_flag']

    name = 'experiment'
    sub_funcs = {
            "DATAPATH": get_constant_datapath(datapath),
            "MODELPATH": pyr_filename_converter
    }
    create_param_files(name, args, sub_funcs, name_flag=name_flag)

if __name__ == "__main__":
    main()
