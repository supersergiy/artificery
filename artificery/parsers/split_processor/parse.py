import torch
import six
from scalenet.residuals import combine_residuals

class SplitProcessor(torch.nn.Module):
    def __init__(self, processors):
        super().__init__()

        self.proc_ranges = []
        for i in range(len(processors)):
            proc = processors[i]
            if 'fm_range' in proc:
                proc_range = [proc['fm_range']]
            elif 'fm_ranges' in proc:
                proc_range = proc['fm_ranges']
            else:
                raise Exception("Split processor range \
                        unspecified: {}".format(proc))

            self.proc_ranges.append(proc_range)

        self.processors = torch.nn.ModuleList([processors[i]['module'] for i in range(len(processors))])

    def forward(self, x, *kargs, **kwargs):
        result_pieces = []
        for i in range(len(self.processors)):
            proc_fms = []
            for r in self.proc_ranges[i]:
                proc_fms += list(range(r[0], r[1]))

            x_piece = x[:, proc_fms]
            #print (x_piece.shape)
            result_piece = self.processors[i](x_piece, *kargs, **kwargs)
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
