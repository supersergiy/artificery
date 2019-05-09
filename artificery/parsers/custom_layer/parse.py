import sys
import importlib

def parse(params, create_module):
    for lib in params['import']:
        module = importlib.import_module(lib)
        globals()[lib] = module

    exec(params['code'], globals())
    if result is None:
        raise Exception("The code argument did not assign a value to 'result' variable")
    return result
