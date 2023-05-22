from pylib import testcaseLib
from pylib import global_var
import pandas

build, env, suite_to_run = testcaseLib.get_input()

if global_var.framework == "yaml":
    result_list = testcaseLib.run_yaml_suite(suite_to_run)
elif global_var.framework == "robot":
    result_list = testcaseLib.run_robot_suite(suite_to_run)
else:
    result_list = []

dataframe = pandas.DataFrame(result_list)
dataframe.to_csv(global_var.log_location + "/result.csv")

# testcaseLib.send_email(global_var.sender_email_id, sender_email_id_password, global_var.receiver_email_id, "test mail")
