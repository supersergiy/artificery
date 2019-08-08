import torch
import copy

class MaskedNormalize(torch.nn.Module):
    def __init__(self, mask_value=0, mask_type='eq', mask_fill=None,
                per_channel_mean=True, per_channel_var=False):
        super().__init__()
        self.mask_value = mask_value
        self.mask_type = mask_type
        self.mask_fill = mask_fill
        self.per_channel_mean = per_channel_mean
        self.per_channel_var = per_channel_var

    def get_mask(self, x):
        if self.mask_type == 'eq':
            return x == self.mask_value
        elif self.mask_type == 'lt':
            return x < self.mask_value
        elif self.mask_type == 'gt':
            return x > self.mask_value
        elif self.mask_type == 'lte':
            return x <= self.mask_value
        elif self.mask_type == 'gte':
            return x >= self.mask_value
        else:
            raise Exception("Maks type unknown: {}".format(mask_type))

    def forward(self, x, eps=1e-5):
        x_out = x.clone()
        mask = self.get_mask(x) == False
        for b in range(x.shape[0]):
            x = x_out[b]
            if self.per_channel_mean and len(x.shape) == 4:
                for f in range(x.shape[1]):
                    m = mask[b, f]
                    x[f][m] = x[f][m].clone() - torch.mean(x[f][m].clone())
            else:
                m = mask[b]
                x[m] = x[m].clone() - torch.mean(x[m].clone())

            if self.per_channel_var and len(x.shape) == 4:
                for f in range(x.shape[1]):
                    m = mask[b, f]
                    var = torch.var(x[f][m].clone())
                    x[f][m] = x[f][m].clone() / (torch.sqrt(var) + eps)
            else:
                m = mask[b]
                var = torch.var(x[m].clone())
                x[m] = x[m].clone() / (torch.sqrt(var) + eps)

        if self.mask_fill is not None:
            x_out[mask == False] = self.mask_fill

        return x_out

def parse(params, create_module):
    params_tmp = copy.deepcopy(params)
    del params_tmp['type']
    net = MaskedNormalize(**params_tmp)
    return net
