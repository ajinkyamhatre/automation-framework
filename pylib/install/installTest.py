from pylib import global_var


def install_kit(node, machine_type):
    global_var.logger.info('node =' + str(node))
    global_var.logger.info('machine_type =' + machine_type)
    # check if kit exists
    return True


def uninstall_kit(keep_kit):
    if keep_kit:
        # keep kit in list
        pass
    else:
        # delete kit
        pass
    return True
