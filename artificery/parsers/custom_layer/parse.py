import sys
import importlib

def parse(params, create_module):
    for lib in params['import']:
        module = importlib.import_module(lib)
        globals()[lib] = module

    return exec(params['code'], globals())
