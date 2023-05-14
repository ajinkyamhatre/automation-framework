import os

import DjangoApp.settings


def get_module_list():
    return os.listdir(DjangoApp.settings.FRAMEWORK_PATH + "\\testcases")


