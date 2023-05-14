from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from QeUI.testLib import get_module_list


def index_page(request):
    context = {"module_list": get_module_list()}
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render(context))
# Create your views here.
