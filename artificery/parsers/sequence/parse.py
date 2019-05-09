import torch

def parse(params, create_module):
    layer_list = []
    modules = [create_module(m) for m in params['arch_desc']['module_list']]

    net = torch.nn.Sequential(*modules)
    return net
