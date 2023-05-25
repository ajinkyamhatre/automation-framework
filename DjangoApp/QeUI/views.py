import os.path

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import sys

from DjangoApp import settings
from .forms import SelectSuiteForm, SelectDateForm, get_dynamic_form

sys.path.append(settings.FRAMEWORK_PATH)
from pylib.testcaseLib import get_date_time, get_logs_details, submit_job, get_func_doc


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
        year, month, day = request.POST["year"], request.POST["month"], request.POST["day"]
        print(year, month, day)
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
            text = log_file.read()
    return HttpResponse(text.replace("\n", "</br></br>"))


def create_testcase(request):
    form_spec = get_func_doc("pylib.install.installTest", "install_kit")
    form = get_dynamic_form(form_spec)
    context = {"form": form}
    return render(request, "create_testcase.html", context)

