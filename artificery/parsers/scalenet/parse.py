import scalenet
import six

def parse(params, create_module):
    if 'max_level' in params:
        net = scalenet.ScaleNet(max_level=params['max_level'])
    else:
        net = scalenet.ScaleNet()

    if "downmodules" in params:
        for level, spec in six.iteritems(params["downmodules"]):
            module = create_module(spec)
            net.set_downmodule(module, level)

    if "upmodules" in params:
        for level, spec in six.iteritems(params["upmodules"]):
            module = create_module(spec)
            net.set_upmodule(module, level)

    if "uplinks" in params:
        if "all" in params["uplinks"]:
            spec = params["uplinks"]["all"]
            module = create_module(spec)
            net.set_all_uplinks(module)
        else:
            for level, spec in six.iteritems(params["uplinks"]):
                module = create_module(spec)
                net.set_uplink(module, level)

    if "downlinks" in params:
        if "all" in params["downlinks"]:
            spec = params["downlinks"]["all"]
            module = create_module(spec)
            net.set_all_downlinks(module)
        else:
            for level, spec in six.iteritems(params["downlinks"]):
                module = create_module(spec)
                net.set_downlink(module, level)

    if "skiplinks" in params:
        if "all" in params["skiplinks"]:
            spec = params["skiplinks"]["all"]
            module = create_module(spec)
            net.set_all_skiplinks(module)
        else:
            for level, spec in six.iteritems(params["skiplinks"]):
                module = create_module(spec)
                net.set_skiplink(module, level)

    if "combiners" in params:
        if "all" in params["combiners"]:
            spec = params["combiners"]["all"]
            module = create_module(spec)
            net.set_all_combiners(module)
        else:
            for level, spec in six.iteritems(params["combiners"]):
                module = create_module(spec)
                net.set_combiner(module, level)

    return net
