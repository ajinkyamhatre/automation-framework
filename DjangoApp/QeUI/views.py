import os.path

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import sys

from DjangoApp import settings
from .forms import SelectSuiteForm, SelectDateForm, get_dynamic_form, parse_form_data

sys.path.append(settings.FRAMEWORK_PATH)
from pylib.testcaseLib import get_date_time, get_logs_details, submit_job, get_func_doc, get_function_to_module_map, create_suite
from pylib.configLib import get_spec_file
import pylib.global_var


def index_page(request):
    context = {"form": SelectSuiteForm()}
    if request.POST:
        submit_job(settings.FRAMEWORK_PATH, dict(request.POST))
        return redirect(logs_view)
    return render(request, "run.html", context)


def logs_view(request):
    year, month, day, *_ = get_date_time()
    date_form = SelectDateForm()
    if request.POST:
        year, month, day = request.POST["date_year"][0], request.POST["date_month"][0], request.POST["date_day"][0]
    path = os.path.join(settings.FRAMEWORK_PATH, f"logs/{year}/{month}/{day}")
    context = {"log_folder_list": get_logs_details(path), "date_form": date_form}
    return render(request, "logs.html", context)


def setup_view(request):
    template = loader.get_template("setup.html")
    return HttpResponse(template.render())


def logs_details(request, log_location):
    text = "log not found!"
    module_folder = os.listdir(log_location)[0]
    log_location = os.path.join(log_location, module_folder)
    if os.path.exists(log_location + "/test.log"):
        with open(log_location + "/test.log") as log_file:
            text = log_file.read().replace("\n", "</br></br>")
    elif os.path.exists(log_location + "/log.html"):
        with open(log_location + "/log.html", encoding="utf8") as fd:
            text = fd.read()
    return HttpResponse(text)


def testcase_list_view(request):
    function_to_module_map = get_function_to_module_map(settings.FRAMEWORK_PATH)
    context = {"function_to_module_map": function_to_module_map}
    respo = render(request, "testcase_list.html", context)
    request.session["testcases"] = list()
    return respo


def create_testcase(request, test):
    module = get_function_to_module_map(settings.FRAMEWORK_PATH)[test]
    form_spec = get_func_doc(module, test)
    form = get_dynamic_form(form_spec)
    if request.POST:
        request.session["testcases"] = request.session["testcases"] + [parse_form_data(form_spec, dict(request.POST))]
    context = {"form": form, "testcases": request.session["testcases"], "test": test}
    return render(request, "create_testcase.html", context)


def create_suite_view(request, test):
    suite_name = request.POST.get("suite_name")
    create_suite(test, request.session["testcases"], suite_name, settings.FRAMEWORK_PATH)
    return redirect(index_page)


def testbed_spec_view(request):
    spec_data = get_spec_file(pylib.global_var.release, settings.FRAMEWORK_PATH)
    spec_forms = {key: get_dynamic_form(value) for key, value in spec_data.items()}
    context = {"spec_forms": spec_forms}
    return render(request, "testbed_spec.html", context)

def jenkins_view(request):
    context = {"spec_forms": spec_forms}
    return render(request, "jenkins.html", context)



