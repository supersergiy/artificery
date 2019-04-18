from scalenet import Sequence

def parse(params, create_module):
    if params["type"] != "ConvBlock":
        raise Exception("ConvBlock parser called for {} type!".format(params["type"]))

    net = Sequence(params["arch_desc"])
    return net
