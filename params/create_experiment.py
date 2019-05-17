import argparse
import os

from creator import create_param_files, get_setting_filename

def get_model_filename_converter(name):
    def model_filename_converter(setting):
        return get_setting_filename(name, setting,
                custom_folder="~/artificery/params/")
    return model_filename_converter

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
    parser.add_argument("--model", type=str, default='pyramid_categorical')
    parser.add_argument("--name_flag", type=str, default=None, required=False)

    args = vars(parser.parse_args())
    datapath = args['datapath']
    del args['datapath']
    name_flag = args['name_flag']
    model = args['model']
    del args['name_flag']
    del args['model']

    name = 'experiment'
    sub_funcs = {
            "DATAPATH": get_constant_datapath(datapath),
            "MODELPATH": get_model_filename_converter(model)
    }
    create_param_files(name, args, sub_funcs, name_flag=name_flag, name_suffix=model)

if __name__ == "__main__":
    main()
