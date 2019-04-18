import torch
import scalenet import UpsampleResiduals

class RollbackWarp(object):
    def __init__(self, rollback_range):
        self.rollback_range = rollback_range
        self.ups_res = UpsampleResiduals()
        self.ups_img = torch.nn.Upsample(scale_factor=2, mode='bilinear')

    def forward(self, x, res, level, up_result):
        #TODO: test whether this is good enough
        for _ in range(self.rollback_range):
            x = self.ups_img(x)
            res  = self.ups_res(res)

        result = res_warp_img(x, res, is_pix_res=True)

        for _ in range(self.rollback_range):
            result = self.downs_img(result)

        return result
