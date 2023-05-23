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
