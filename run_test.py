import argparse
import json
import logging

def get_logger():
# Create and configure logger
    logging.basicConfig(filename="newfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    return logger

def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build")
    parser.add_argument("--env")
    parser.add_argument("--suite")
    args = parser.parse_args()
    return args.build, args.env, args.suite


def get_testcase(suite_file):
    with open("testcases/" + suite_file) as json_file:
        suite_details = json.load(json_file)
    return suite_details


build, env, suite = get_input()
logger = get_logger()

logger.info(f"Build: {build}, Env: {env}, Suite: {suite}")
suite_details = get_testcase(suite)

suite_name = suite_details["suite name"]

logger.info(f"Suite Name: {suite_name}")

for test_details in suite_details["test cases"]:
    logger.info(f"running test case: {test_details['test cases']}")
    


