import logging
import argparse
import yaml
from pylib import global_var
import smtplib
import os
import datetime
import robot
import time


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
    parser.add_argument("--sender_email_id_password")
    args = parser.parse_args()
    return args.build, args.env, args.suite, args.sender_email_id_password


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
    suite_name = suite_details["suite name"]
    create_log_dir(suite_name)
    logger = get_logger()
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
        logger.info(f"Test suite executed in: {current_time - suite_start_time} sec.")
    return result_list


def get_module_list(path):
    return os.listdir(path + "/testcases")


def get_module_details(path):
    return {module: get_testcase(module, path) for module in get_module_list(path)}


def get_logs_details(path):
    if os.path.exists(path):
        return os.listdir(path)
    else:
        return []


def submit_job(framework_path, job):
    job_path = os.path.join(framework_path, "jobs")
    job_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S") + ".yaml"
    print(job_name)
    with open(os.path.join(job_path, job_name), "w") as yaml_file:
        yaml.dump(job, yaml_file)


def run(job):
    pid = os.system(" ".join(["./run_test.py",
                              "--build", job["build"],
                              "--env", job["env"],
                              "--suite", job["suite"],
                              "--sender_email_id_password", job["sender_email_id_password"]]))
    return pid


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
