import logging
import argparse
import yaml
from pylib import global_var
import smtplib
import os
import datetime
import robot
import time
import pandas
from inspect import getmembers, isfunction


def run_robot_suite(testcases_file):
    create_log_dir(testcases_file)
    logfile = open(global_var.log_location + '/robot.log', 'w')
    output = robot.run(f"robot-testcases/{testcases_file}", outputdir=global_var.log_location, stdout=logfile)
    print("************************************** robot output **************************************")
    print(output)
    logfile.close()
    return []


def get_date_time():
    # using now() to get current time
    current_time = datetime.datetime.now()
    return current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second


def get_logger():
    # Create and configure logger
    logging.basicConfig(filename=f"{global_var.log_location}/test.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    # Creating an object
    global_var.logger = logging.getLogger()
    # Setting the threshold of logger to DEBUG
    global_var.logger.setLevel(global_var.LOG_LEVEL_MAP[global_var.logging_level])
    return global_var.logger


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode")
    parser.add_argument("--build")
    parser.add_argument("--env")
    parser.add_argument("--suite")
    args = parser.parse_args()
    return args.mode, args.build, args.env, args.suite


def get_testcase(suite_file, path):
    with open(os.path.join(path + "/testcases/", suite_file)) as yaml_file:
        suite_details = yaml.safe_load(yaml_file)
    return suite_details


def send_email(receiver_email_id, message):
    # creates SMTP session
    smtp = smtplib.SMTP(global_var.mail_server, 587)

    # start TLS for security
    smtp.starttls()

    # Authentication
    smtp.login(global_var.sender_email_id, global_var.sender_email_id_password)

    # sending the mail
    smtp.sendmail(msg=message.encode(), from_addr=global_var.sender_email_id, to_addrs=receiver_email_id)

    # terminating the session
    smtp.quit()


def create_log_dir(suite_name):
    year, month, day, hour, minute, second = get_date_time()
    global_var.log_location = f"logs/{year}/{month}/{day}/{hour}-{minute}-{second}/{suite_name}"
    os.makedirs(global_var.log_location, mode=0o777, exist_ok=True)


def run_yaml_suite(suite):
    suite_details = get_testcase(suite, ".")
    suite_name = suite_details["suite"]
    create_log_dir(suite_name)
    logger = get_logger()
    logger.info(f"Suite Name: {suite_name}")
    current_time = start_time = suite_start_time = time.time()
    result_list = list()
    for test_details in suite_details["testcases"]:
        logger.info(f"running test case: {test_details['testname']}")
        import_statement = f"from {test_details['module']} import {test_details['test']}"
        logger.debug(import_statement)
        exec(import_statement)
        function_call = f"{test_details['test']}(**{test_details['testspec']})"
        logger.debug(function_call)
        result = eval(function_call)
        current_time = time.time()
        logger.info(f"Test case executed in: {current_time - start_time} sec.")
        result_list.append({
            "Testcase": test_details['testname'],
            "Result": "PASS" if result else "FAIL",
            "Execution Time": current_time - start_time
        })
        start_time = current_time
        logger.info(f"Test suite executed in: {current_time - suite_start_time} sec.")
    return result_list


def get_module_list(path):
    framework_to_testcase_map = {
        "yaml": "/testcases",
        "robot": "/robot-testcases",
    }
    return os.listdir(path + framework_to_testcase_map[global_var.framework])


def get_module_details(path):
    return {module: get_testcase(module, path) for module in get_module_list(path)}


def get_logs_details(path):
    if os.path.exists(path):
        return [(folder, os.path.join(path, folder)) for folder in os.listdir(path)]
    else:
        return []


def submit_job(framework_path, job):
    job_path = os.path.join(framework_path, "jobs")
    job_name = "job-" + datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S") + ".yaml"
    with open(os.path.join(job_path, job_name), "w") as yaml_file:
        yaml.dump(job, yaml_file)


def run_test(build, env, suite_to_run):
    if global_var.framework == "yaml":
        result_list = run_yaml_suite(suite_to_run)
    elif global_var.framework == "robot":
        result_list = run_robot_suite(suite_to_run)
    else:
        result_list = []

    dataframe = pandas.DataFrame(result_list)
    dataframe.to_csv(global_var.log_location + "/result.csv")

    # testcaseLib.send_email(global_var.sender_email_id, sender_email_id_password, global_var.receiver_email_id, "test mail")


def get_job_details(framework_path, job):
    """
    This function returns job details
    :param framework_path: path of automation framework
    :param job: name of job file
    :return: returns details of job in the form of dict
    """
    with open(os.path.join(framework_path + "/jobs/", job)) as yaml_file:
        job_details = yaml.safe_load(yaml_file)
    return job_details


def get_oldest_job():
    """
    This function return first submited job
    :return: job file name
    """
    jobs_list = os.listdir("jobs")
    if jobs_list:
        jobs_list.sort()
        return jobs_list[0]


def get_func_doc(module, test):
    """
    This function is used to get list of param of particular function for creating form.
    :param module: module name
    :param test: test function name
    :return: doc string in the form of dict
    """
    import_statement = f"from {module} import {test}"
    exec(import_statement)
    doc = eval(f"{test}.__doc__")
    return yaml.safe_load(doc)


def get_function_list(module):
    """
    This function is used to return list of function defined in given module
    :param module: complete path of a module
    :return: list of function defied in that module
    """
    exec(f"import {module}")
    return getmembers(eval(module), isfunction)


def get_function_to_module_map(framework_path):
    """
    this function returns function to module map
    :return:
    """
    function_to_module_map = dict()
    for module in os.listdir(framework_path + "/pylib/testcaseDef"):
        module_full_path = f"pylib.testcaseDef.{module.split('.py')[0]}"
        for func in get_function_list(module_full_path):
            function_to_module_map[func[0]] = module_full_path
    return function_to_module_map


def create_suite(test, test_data, suite_name, framework_path):
    module = get_function_to_module_map(framework_path)[test]
    test_suite = {
        "suite": suite_name,
        "testcases": []
    }
    for test_spec in test_data:
        test_name = test_spec["name"]
        del test_spec["name"]
        test_suite["testcases"].append({
                                        "module": module,
                                        "test": test,
                                        "testname": test_name,
                                        "testspec": test_spec
                                        })
    yaml_target_path = framework_path + f"/testcases/{suite_name.strip().replace(' ', '_')}.yaml"
    with open(yaml_target_path, 'w') as file:
        yaml.dump(test_suite, file)


if __name__ == "__main__":
    pass
