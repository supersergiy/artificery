from .rollback_warp import RollbackWarp

def parse(params, create_module):
    rollback_range = params['arch_desc']['rollback']
    net = RollbackWarp(rollback_range)
    return net
