import logging
import argparse
import json
from pylib import global_var
import smtplib
import os


def get_logger(suite_name):
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


def get_testcase(suite_file):
    with open("testcases/" + suite_file) as json_file:
        suite_details = json.load(json_file)
    return suite_details


def send_email(sender_email_id, receiver_email_id, message):
    # creates SMTP session
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    smtp.starttls()

    # Authentication
    smtp.login("softwaretechmart@gmail.com", "sender_email_id_password")

    # sending the mail
    smtp.sendmail(sender_email_id, receiver_email_id, message)

    # terminating the session
    smtp.quit()
