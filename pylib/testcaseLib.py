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
    global_var.logger.setLevel(global_var.logging_level_map[global_var.logging_level])
    return global_var.logger


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build")
    parser.add_argument("--env")
    parser.add_argument("--suite")
    args = parser.parse_args()
    return args.build, args.env, args.suite


def get_testcase(suite_file, path):
    with open(os.path.join(path + "/testcases/", suite_file)) as yaml_file:
        suite_details = yaml.safe_load(yaml_file)
    return suite_details


def send_email(sender_email_id, sender_email_id_password, receiver_email_id, message):
    # creates SMTP session
    smtp = smtplib.SMTP('smtp-relay.sendinblue.com', 587)

    # start TLS for security
    smtp.starttls()

    # Authentication
    smtp.login(sender_email_id, sender_email_id_password)

    # sending the mail
    smtp.sendmail(msg=message.encode(), from_addr=sender_email_id, to_addrs=receiver_email_id)

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
    return os.listdir(path + "/testcases")


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
    with open(os.path.join(framework_path + "/jobs/", job)) as yaml_file:
        job_details = yaml.safe_load(yaml_file)
    return job_details


def get_oldest_job():
    jobs_list = os.listdir("jobs")
    if jobs_list:
        jobs_list.sort()
        return jobs_list[0]


if __name__ == "__main__":
    pass
