import os

import DjangoApp.settings
import json


def get_module_list():
    return os.listdir(DjangoApp.settings.FRAMEWORK_PATH + "\\testcases")


def get_module_details():
    return {module: get_testcase(module) for module in get_module_list()}


def get_testcase(suite_file):
    with open(DjangoApp.settings.FRAMEWORK_PATH + "/testcases/" + suite_file) as json_file:
        suite_details = json.load(json_file)
    return suite_details
