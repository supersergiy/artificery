from scalenet import Sequence

def parse(params, create_module):
    net = Sequence(params["arch_desc"])
    return net
