import torch
from scalenet import Model

class TransparentSeq(Model):
    def __init__(self, stages):
        super().__init__()
        self.stages = torch.nn.ModuleList(stages)
        self.inermediate = []

    def forward(self, x, start_stage=None, end_stage=None):
        self.intermediate = []
        if start_stage is None:
            start_stage = 0
        if end_stage is None:
            end_stage = len(self.stages)

        for i in range(start_stage, end_stage):
            m = self.stages[i]
            x = m(x)
            self.intermediate.append(x)

        return self.intermediate[-1]

def parse(params, create_module):
    layer_list = []
    module_specs = params["modules"]

    modules = [create_module(m) for m in params['modules']]

    net = TransparentSeq(modules)
    return net
