import torch
from scalenet.residuals import combine_residuals

class FmRangeApply(torch.nn.Module):
    def __init__(self, module, fm_range):
        super().__init__()
        self.module = module
        self.fm_range = fm_range

    def forward(self, x, *kargs, **kwargs):
        b_in, c_in, *rest_in = x.shape
        assert c_in % self.fm_range == 0
        x_per_fm = x.view(b_in * (c_in // self.fm_range), self.fm_range, *rest_in)
        out_per_fm = self.module(x_per_fm)
        b_out, c_out, *rest_out = out_per_fm.shape
        out = out_per_fm.view(b_in, -1, *rest_out)

        return out

def parse(params, create_module):
    inner_module = params['module']
    fm_range = params['fm_range']
    net = FmRangeApply(create_module(inner_module), fm_range)
    return net
