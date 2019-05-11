import copy
import six
import os

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

def get_setting_filename(name, setting, name_flag=None, custom_folder=None):
    filename = name
    for k, v in sorted(six.iteritems(setting)):
        filename += '_{}{}'.format(k, v)
    if name_flag is not None:
        filename += '_{}'.format(name_flag)
    filename += '.json'

    if custom_folder is None:
        result = os.path.join(name, filename)
    else:
        result = os.path.join(custom_folder, filename)
    return result

def create_param_files(name, args, sub_funcs={}, name_flag=None):
    template_path = './templates/{}.json'.format(name)
    with open(template_path, 'r') as f:
        template_lines = []
        for l in f:
            template_lines.append(l)
    combos = get_all_combinations(args)
    for setting in combos:
        filename = get_setting_filename(name, setting, name_flag=name_flag)
        if len(sub_funcs) == 0:
            replace_dict = setting
        else:
            replace_dict = {}
            for sub_name, func in six.iteritems(sub_funcs):
                replace_dict[sub_name] = func(setting)

        with open(filename, 'w') as f:
            for l in template_lines:
                f.write(replace_all(l, replace_dict, key_to_upper=True))


