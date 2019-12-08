import torch
import six
from scalenet.residuals import combine_residuals

class SplitProcessor(torch.nn.Module):
    def __init__(self, processors):
        super().__init__()

        self.fm_ranges = [processors[i]['fm_range'] for i in range(len(processors))]
        self.processors = torch.nn.ModuleList([processors[i]['module'] for i in range(len(processors))])

    def forward(self, x):
        result_pieces = []
        for i in range(len(self.processors)):
            x_piece = x[:, self.fm_ranges[i][0]:self.fm_ranges[i][1]]
            #print (x_piece.shape)
            result_piece = self.processors[i](x_piece)
            #print (result_piece.shape)
            result_pieces.append(result_piece)

        result = torch.cat(result_pieces, dim=1)
        #print (result.shape)

        return result

def parse(params, create_module):
    processors = params['processors']
    for p in processors:
        p['module'] = create_module(p['module'])
    net = SplitProcessor(processors)
    return net
