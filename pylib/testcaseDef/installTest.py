from pylib import global_var
import time


def install_kit(node, machine_type):
    """
    node:
        type: IntegerField
        label: No of Nodes
        choices:
    machine_type:
        type: ChoiceField
        label: Machine Type
        choices:
            - bm
            - virtual
    """
    global_var.logger.info('node =' + str(node))
    global_var.logger.info('machine_type =' + machine_type)
    time.sleep(3)
    # check if kit exists
    return True


def uninstall_kit(keep_kit):
    """
    keep_kit:
        type: BooleanField
        label: Do not delete setup
        choices:
    """
    if keep_kit:
        # keep kit in list
        pass
    else:
        # delete kit
        pass
    return True

