from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.index_page, name="dashboard"),
    path("logs/", views.logs_view, name="logs"),
    path("logDetails/<path:log_location>", views.logs_details, name="logDetails"),
    path("createTest/", views.create_testcase, name="createTest")


]
