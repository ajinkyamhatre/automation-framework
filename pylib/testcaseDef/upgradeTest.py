from pylib import global_var
import time


def upgrade(node, machine_type):
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
