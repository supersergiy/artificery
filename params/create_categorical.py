import argparse
import copy
import six
#from .creator import create_param_files

def get_all_combinations(x):
    x = copy.deepcopy(x)

    if isinstance(x, dict):
        keys = x.keys()
        if len(keys) == 0:
            return [{}]
        else:
            k, kv = x.popitem()
            k_result = get_all_combinations(x)
            result = []
            if isinstance(kv, list):
                for i in kv:
                    for entry in k_result:
                        my_entry = copy.deepcopy(entry)
                        my_entry[k] = i
                        result.append(my_entry)
            else:
                for entry in k_result:
                    my_entry = copy.deepcopy(entry)
                    my_entry[k] = kv
                    result.append(my_entry)
            return result

    else:
        raise Exception("Wut Wut")

def replace_all(text, dic, key_to_upper=False):
    for i, j in six.iteritems(dic):
        if key_to_upper:
            i = i.upper()
        text = text.replace(i, j)
    return text

def get_setting_filename(name, setting):
    filename = name
    for k, v in six.iteritems(setting):
        filename += '_{}{}'.format(k, v)
    filename += '.json'
    return filename

def create_param_files(name, args):
    template_path = './templates/{}.json'.format(name)
    with open(template_path, 'r') as f:
        template_lines = []
        for l in f:
            template_lines.append(l)
    combos = get_all_combinations(args)
    for setting in combos:
        filename = get_setting_filename(name, setting)
        with open(filename, 'w') as f:
            for l in template_lines:
                import pdb; pdb.set_trace()
                f.write(replace_all(l, setting))

def main():
    parser = argparse.ArgumentParser()
    args_list = ['compch', 'outch', 'grid', 'step', 'maxvalue', 'trainstep']
    for a in args_list:
        parser.add_argument("--{}".format(a), type=str, nargs='+', required=True)

    args = vars(parser.parse_args())
    name = 'categorical'

    create_param_files(name, args)

if __name__ == "__main__":
    main()
