import importlib

def parser(params, create_module):
    for lib in params['import']:
        importlib.import_module(lib)

    return exec(params['code'])
