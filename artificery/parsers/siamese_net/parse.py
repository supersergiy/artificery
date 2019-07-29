import torch
from scalenet.residuals import combine_residuals

class SiameseNet(torch.nn.Module):
    def __init__(self, net):
        super().__init__()
        self.module = net

    def forward(self, x_list):
        return [self.module(x) for x in x_list]

def parse(params, create_module):
    net = params['arch_desc']['net']
    siam = SiameseNet(create_module(net))
    return siam
