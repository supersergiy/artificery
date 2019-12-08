import torch
import copy

class MaskOutputBasedOnInput(torch.nn.Module):
    def __init__(self, inner_module, mask_value=0, mask_type='eq', mask_fill=0):
        super().__init__()
        self.mask_value = mask_value
        self.mask_type = mask_type
        self.mask_fill = mask_fill
        self.inner_module = inner_module

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

    def downsample(self, x, target_shape):
        assert len(target_shape) == 4
        assert len(x.shape) == 4
        assert target_shape[0:2] == x.shape[0:2]
        assert target_shape[2] == target_shape[3]
        assert x.shape[2] == x.shape[3]
        assert x.shape[2] % target_shape[2] == 0
        ratio = x.shape[2] // target_shape[2]

        result = x.clone()
        #result = torch.nn.functional.max_pool2d(result, ratio)
        result = torch.nn.functional.avg_pool2d(result, ratio) == 1.0
        result = result.type(x.type())

        if result.shape != target_shape:
            import pdb; pdb.set_trace()
            raise Exception("Can't downsample {} to {}".format(x.shape, target_shape))
        return result

    def forward(self, x):
        y = self.inner_module(x)
        x_mask = self.get_mask(x)
        y_mask = self.downsample(x_mask.float(), y.shape).byte()
        y[y_mask] = self.mask_fill
        return y

def parse(params, create_module):
    inner_module = create_module(params['inner_module'])
    params_tmp = copy.deepcopy(params)
    del params_tmp['type']
    del params_tmp['inner_module']
    net = MaskOutputBasedOnInput(inner_module=inner_module, **params_tmp)
    return net
