import torch
from scalenet import UpsampleResiduals
from scalenet.residuals import res_warp_img

class RollbackWarp(torch.nn.Module):
    def __init__(self, rollback_range):
        super().__init__()
        self.rollback_range = rollback_range
        self.ups_res = UpsampleResiduals()
        self.ups_img = torch.nn.Upsample(scale_factor=2, mode='bilinear')
        self.downs_img = torch.nn.AvgPool2d(2)

    def forward(self, x, res, state, level):
        if len(torch.nonzero(res))  == 0: #res is all 0's
            return x

        res = res.permute(0, 2, 3, 1)

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
