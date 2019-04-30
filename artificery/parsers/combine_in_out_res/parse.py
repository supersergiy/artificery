import torch
from scalenet.residuals import combine_residuals, upsample_residuals

class CombinInOutRes(torch.nn.Module):
    def __init__(self, rollback_range):
        super().__init__()

    def forward(self, x, res, level, up_result):
        #TODO: test whether this is good enough
        for _ in range(self.rollback_range):
            x = self.ups_img(x)
            res  = self.ups_res(res)

        result = res_warp_img(x, res, is_pix_res=True)

        for _ in range(self.rollback_range):
            result = self.downs_img(result)

        return result

def parse(params, create_module):
    rollback_range = params['arch_desc']['rollback']
    net = RollbackWarp(rollback_range)
    return net
