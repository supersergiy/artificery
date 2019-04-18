import torch

def parse(params, create_module):
    if 'scale' in params:
        scale = params['scale']
    else:
        scale = 2

    if 'mode' in params:
        mode = params['mode']
    else:
        mode = 'bilinear'

    return torch.nn.Upsample(scale_factor=scale, mode=mode)
