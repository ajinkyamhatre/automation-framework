import os.path

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sys

from DjangoApp import settings
from .forms import SelectSuiteForm

sys.path.append(settings.FRAMEWORK_PATH)
from pylib.testcaseLib import get_date_time, get_logs_details, submit_job


def index_page(request):
    context = {"form": SelectSuiteForm()}
    if request.POST:
        submit_job(settings.FRAMEWORK_PATH, dict(request.POST))
        # redirect to run route
    return render(request, "run.html", context)


def logs_view(request):
    year, month, day, *_ = get_date_time()
    path = os.path.join(settings.FRAMEWORK_PATH, f"logs/{year}/{month}/{day}")
    context = {"log_folder_list": get_logs_details(path)}
    template = loader.get_template("logs.html")
    return HttpResponse(template.render(context))


def setup_view(request):
    template = loader.get_template("setup.html")
    return HttpResponse(template.render())
