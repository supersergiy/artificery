import argparse
import os

from creator import create_param_files, get_setting_filename

def cat_filename_converter(setting):
    return get_setting_filename('categorical', setting)

def main():
    parser = argparse.ArgumentParser()
    args_list = ['compch', 'outch', 'grid', 'step', 'maxvalue', 'trainst']
    for a in args_list:
        parser.add_argument("--{}".format(a), type=str, nargs='+', required=True)

    args = vars(parser.parse_args())

    name = 'm4_categorical'

    create_param_files(name, args, sub_funcs={'CATEGORIZER': cat_filename_converter})

if __name__ == "__main__":
    main()
