import argparse
from creator import create_param_files

def main():
    parser = argparse.ArgumentParser()
    args_list = ['compch', 'outch', 'grid', 'step', 'maxvalue', 'trainst']
    for a in args_list:
        parser.add_argument("--{}".format(a), type=str, nargs='+', required=True)

    args = vars(parser.parse_args())
    name = 'categorical'

    create_param_files(name, args)

if __name__ == "__main__":
    main()
