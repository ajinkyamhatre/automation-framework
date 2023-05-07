from pylib import testcaseLib
from pylib import global_var
import time
import pandas


build, env, suite = testcaseLib.get_input()

suite_details = testcaseLib.get_testcase(suite)

suite_name = suite_details["suite name"]
testcaseLib.create_log_dir(suite_name)
logger = testcaseLib.get_logger()
logger.info(f"Suite Name: {suite_name}")
current_time = start_time = suite_start_time = time.time()
result_list = list()
for test_details in suite_details["test cases"]:
    logger.info(f"running test case: {test_details['test name']}")
    import_statement = f"from {test_details['module']} import {test_details['test']}"
    logger.debug(import_statement)
    exec(import_statement)
    function_call = f"{test_details['test']}(**{test_details['testspec']})"
    logger.debug(function_call)
    result = eval(function_call)
    current_time = time.time()
    logger.info(f"Test case executed in: {current_time - start_time} sec.")
    result_list.append({
        "Testcase": test_details['test name'],
        "Result": "PASS" if result else "FAIL",
        "Execution Time": current_time - start_time
    })
    start_time = current_time

dataframe = pandas.DataFrame(result_list)
print(dataframe)
dataframe.to_csv(global_var.log_location + "/result.csv")
logger.info(f"Test suite executed in: {current_time - suite_start_time} sec.")
