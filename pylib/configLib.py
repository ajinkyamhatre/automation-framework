import os
import yaml


def get_spec_file(release, framework_path="."):
    with open(os.path.join(framework_path + "/testbed/" + release, "testbed-spec.yaml")) as yaml_file:
        testbed_spec = yaml.safe_load(yaml_file)
    return testbed_spec


def add_component():
    pass


def delete_component():
    pass


def update_component():
    pass

