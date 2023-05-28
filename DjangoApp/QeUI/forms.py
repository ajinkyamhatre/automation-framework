# import the standard Django Forms
# from built-in library
from django import forms
import sys
from DjangoApp import settings

sys.path.append(settings.FRAMEWORK_PATH)
from pylib.testcaseLib import get_module_list


# creating a form
class SelectSuiteForm(forms.Form):
    env = forms.ChoiceField(choices=(("virtual", "Virtual"), ("BM", "BM")))
    build = forms.IntegerField()
    suite = forms.ChoiceField(choices=((suite, suite) for suite in get_module_list(settings.FRAMEWORK_PATH)))


class SelectDateForm(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)


def get_dynamic_form(param_dict):
    form_params = {"name": forms.CharField()}
    for param, param_spec in param_dict.items():
        if param_spec['type'].strip() == "ChoiceField":
            form_params[param] = eval(f"forms.{param_spec['type']}(label='{param_spec['label']}', choices={tuple((c, c) for c in param_spec['choices'])})")
        else:
            form_params[param] = eval(f"forms.{param_spec['type']}(label='{param_spec['label']}')")
    dynamicForm = type("dynamicForm", (forms.Form,), form_params)
    return dynamicForm


def parse_form_data(form_spec, form_data):
    parsed_data = {
        "name": form_data["name"][0]
    }
    for field in form_spec:
        parsed_data[field] = form_data[field][0]
    return parsed_data