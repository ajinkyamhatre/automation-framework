from pylib import testcaseLib
from pylib import global_var
import time
import pandas


build, env, suite = testcaseLib.get_input()

suite_details = testcaseLib.get_testcase(suite)

suite_name = suite_details["suite name"]
logger = testcaseLib.get_logger(suite_name)
logger.info(f"Suite Name: {suite_name}")
current_time = start_time = suite_start_time = time.time()

for test_details in suite_details["test cases"]:
    logger.info(f"running test case: {test_details['test name']}")
    import_statement = f"from {test_details['module']} import {test_details['test']}"
    logger.debug(import_statement)
    exec(import_statement)
    function_call = f"{test_details['test']}(**{test_details['testspec']})"
    logger.debug(function_call)
    eval(function_call)
    current_time = time.time()
    logger.info(f"Test case executed in: {current_time - start_time} sec.")
    start_time = current_time
logger.info(f"Test suite executed in: {current_time - suite_start_time} sec.")
