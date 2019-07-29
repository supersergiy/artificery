import torch
from scalenet import Model

class ModelWithWeights(Model):
    def __init__(self, m, num_weights):
        super().__init__()
        self.m = m
        self.weights = torch.nn.Parameter(torch.cuda.FloatTensor([1.0 for i in range(num_weights)]))

    def forward(self, x):
        return self.m(x)

def parse(params, create_module):
    layer_list = []
    model = create_module(params['model'])
    num_weights = params['num_weights']
    net = ModelWithWeights(model, num_weights)
    return net
