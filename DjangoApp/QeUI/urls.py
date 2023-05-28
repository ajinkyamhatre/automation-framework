from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.index_page, name="dashboard"),
    path("logs/", views.logs_view, name="logs"),
    path("logDetails/<path:log_location>", views.logs_details, name="logDetails"),
    path("createTest/<test>", views.create_testcase, name="createTest"),
    path("testcaseList/", views.testcase_list_view, name="testcaseList"),
    path("createSuite/<test>", views.create_suite_view, name="createSuite"),
    path("testbedSpec/", views.testbed_spec_view, name="testbedSpec"),
]
