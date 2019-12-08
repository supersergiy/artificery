import torch

class Vectorizer(torch.nn.Module):
    def __init__(self, out_channels=2, component_channels=7,
                 grid=False, norm_method='softmax',
                 permute=True, step=None,
                 max_value=None,
                 train_step=False):
        super(Vectorizer, self).__init__()

        if step is not None and max_value is not None:
            raise Exception("Ambiguous specification for categorical regression: "
                    "both step and max_value are specified")
        if step is None:
            if max_value is None:
                step = 1
            else:
                step = max_value / (component_channels//2)

        self.out_channels = out_channels
        self.component_channels = component_channels
        self.norm_method = norm_method
        self.permute = permute
        self.grid = grid

        if self.grid:
            x, y = torch.meshgrid([torch.range(0, self.component_channels - 1, device='cuda',
                                 requires_grad=False)]*2
                                 )
            x = x - self.component_channels//2
            y = y - self.component_channels//2

            self.weights = torch.cat((x.unsqueeze(-1), y.unsqueeze(-1)), 2)
            self.weights = self.weights.view(-1, 2)
        else:
            self.weights = torch.range(0, self.component_channels - 1, device='cuda',
                                  requires_grad=False) - self.component_channels//2
            self.weights = self.weights.unsqueeze(-1)

        self.weights *= step

        if train_step:
            self.weights = torch.nn.Parameter(self.weights)

        norm_methods = {
            'softmax': torch.nn.Softmax(-1),
            'softmin': torch.nn.Softmin(-1),
            'norm': torch.nn.LayerNorm(self.component_channels,
                                       eps=1e-05, elementwise_affine=False)
        }
        self.normer = norm_methods[self.norm_method]

    def forward(self, x_in):
        if self.permute:
            x = x_in.permute(0, 2, 3, 1)
        else:
            x = x_in

        if self.grid:
            result = self.grid_forward(x)
        else:
            result = self.channelwise_forward(x)

        if self.permute:
            result = result.permute(0, 3, 1, 2)
        return result

    def channelwise_forward(self, x):
        components = []
        norm_components = []
        result_components = []
        for c_id in range(self.out_channels):
            ch_start = c_id * self.component_channels
            ch_end = (c_id + 1) * self.component_channels
            component = x[..., ch_start:ch_end]
            #print ('Component: ', torch.mean(component))
            norm_component = self.normer(component)
            norm_components.append(norm_component)
            norm_component_2d = norm_component.view(-1, self.component_channels)
            #print (norm_component)
            component_result_2d = torch.mm(norm_component_2d, self.weights)
            component_result = component_result_2d.view(list(component.shape[0:-1]) + [1])
            result_components.append(component_result)

        result = torch.cat(result_components, -1)
        #print ('Result: ', result.shape)
        #print ('Result: ', torch.mean(result))
        return result

    def grid_forward(self, x):
        components = []
        norm_components = []
        result_components = []

        ch_start = 0
        ch_end = self.component_channels**2
        component = x[..., ch_start:ch_end]

        #print ('Component: ', torch.mean(component))
        norm_component = self.normer(component)
        norm_components.append(norm_component)
        norm_component_2d = norm_component.view(-1, self.component_channels**2)
        #print (norm_component)
        component_result_2d = torch.mm(norm_component_2d, self.weights)
        component_result = component_result_2d.view(list(component.shape[0:-1]) + [self.out_channels])
        result_components.append(component_result)

        result = torch.cat(result_components, -1)
        #print ('Result: ', result.shape)
        #print ('Result: ', torch.mean(result))
        return result

def parse(params, create_module):
    params = params['arch_desc']
    net = Vectorizer(**params)
    return net
