# import the standard Django Forms
# from built-in library
from flask_wtf import Form
import sys
import settings
import wtforms

sys.path.append(settings.FRAMEWORK_PATH)
from pylib.testcaseLib import get_module_list
import requests


def get_jenkins_builds():
    builds = [{"number": "007"}]
    try:
        job_details = requests.get(f"{settings.JENKINS}/job/Jarvis-CICD/api/json", auth=(settings.JENKINS_USER, settings.JENKINS_PASSWORD))
        print(job_details)
        builds = job_details.json()["builds"]
    except:
        pass
    return builds


# creating a form
class SelectSuiteForm(Form):
    build = wtforms.SelectField(choices=((build["number"], build["number"]) for build in get_jenkins_builds()))
    suite = wtforms.SelectField(choices=((suite, suite) for suite in get_module_list(settings.FRAMEWORK_PATH)))


class SelectDateForm(Form):
    date = wtforms.DateField()


def get_dynamic_form(param_dict):
    form_params = {"name": wtforms.TextField()}
    for param, param_spec in param_dict.items():
        if param_spec['type'].strip() == "ChoiceField":
            form_params[param] = eval(
                f"forms.{param_spec['type']}(label='{param_spec['label']}', choices={tuple((c, c) for c in param_spec['choices'])})")
        else:
            form_params[param] = eval(f"forms.{param_spec['type']}(label='{param_spec['label']}')")
    dynamicForm = type("dynamicForm", (Form,), form_params)
    return dynamicForm


def parse_form_data(form_spec, form_data):
    parsed_data = {
        "name": form_data["name"][0]
    }
    for field in form_spec:
        parsed_data[field] = form_data[field][0]
    return parsed_data
