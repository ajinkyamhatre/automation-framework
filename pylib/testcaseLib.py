import logging
import argparse
import json
from pylib import global_var
import smtplib
import os
import datetime
import email


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


def get_testcase(suite_file):
    with open("testcases/" + suite_file) as json_file:
        suite_details = json.load(json_file)
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
