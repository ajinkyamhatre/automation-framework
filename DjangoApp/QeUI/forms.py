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
    year = forms.ChoiceField(choices=((y, y) for y in range(2022, 2025)))
    month = forms.ChoiceField(choices=((m, m) for m in range(1, 13)))
    day = forms.ChoiceField(choices=((d, d) for d in range(1, 32)))


def get_dynamic_form(param_dict):
    form_params = dict()
    for param, param_spec in param_dict.items():
        if param_spec['type'].strip() == "ChoiceField":
            form_params[param] = eval(f"forms.{param_spec['type']}(label='{param_spec['label']}', choices={tuple((c, c) for c in param_spec['choices'])})")
        else:
            form_params[param] = eval(f"forms.{param_spec['type']}(label='{param_spec['label']}')")
    dynamicForm = type("dynamicForm", (forms.Form,), form_params)
    return dynamicForm
