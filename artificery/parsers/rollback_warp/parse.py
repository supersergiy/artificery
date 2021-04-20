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
        if res is None or len(torch.nonzero(res))  == 0: #res is all 0's
            return x

        res = res.permute(0, 2, 3, 1)

        #TODO: test whether this is good enough
        #for _ in range(self.rollback_range):
        #    x = self.ups_img(x)
        #    res  = self.ups_res(res)
        #import pdb; pdb.set_trace()
        num_fms = x.shape[1]
        src = x[:, :num_fms//2]
        tgt = x[:, num_fms//2:]
        #print (f"src: {src[:, 0].mean()}, tgt: {tgt[:, 0].mean()}")
        warped_src = res_warp_img(src, res, is_pix_res=True, rollback=self.rollback_range)

        #warped_tgt = res_warp_img(tgt, res, is_pix_res=True, rollback=self.rollback_range)
        result = torch.cat((warped_src, tgt), 1)
        #result = torch.cat((src, warped_tgt), 1)
        #for _ in range(self.rollback_range):
        #    result = self.downs_img(result)

        return result

def parse(params, create_module):
    rollback_range = params['arch_desc']['rollback']
    net = RollbackWarp(rollback_range)
    return net
