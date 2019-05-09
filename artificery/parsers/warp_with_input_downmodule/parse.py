import torch
from scalenet.residuals import combine_residuals

class WarpWithInputDownmodule(torch.nn.Module):
    def __init__(self, inner_module):
        super().__init__()
        self.module = inner_module

    def forward(self, x, state, level):
        my_in = state['down'][str(level)]['input']
        my_out = self.module(x)
        result = combine_residuals(my_out.permute(0, 2, 3, 1),
                                   my_in.permute(0, 2, 3, 1), is_pix_res=True).permute(0, 3, 1, 2)

        return result

def parse(params, create_module):
    inner_module = params['arch_desc']['inner_module']
    net = WarpWithInputDownmodule(create_module(inner_module))
    return net
