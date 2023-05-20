import os.path

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sys

from DjangoApp import settings

sys.path.append(settings.FRAMEWORK_PATH)
from pylib.testcaseLib import get_date_time, get_module_details, get_logs_details


def index_page(request):
    context = {"module_list": get_module_details()}
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render(context))


def logs_view(request):
    year, month, day, *_ = get_date_time()
    path = os.path.join(settings.FRAMEWORK_PATH, f"logs/{year}/{month}/{day}")
    context = {"log_folder_list": get_logs_details(path)}
    print(context)
    template = loader.get_template("logs.html")
    return HttpResponse(template.render(context))
