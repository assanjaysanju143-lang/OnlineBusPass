
from django.urls import path
from . import views

urlpatterns = [
    path("apply/", views.apply_for_pass, name="apply_for_pass"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("my-digital-pass/", views.my_digital_pass, name="my_digital_pass"),
    path("verify/<str:pass_number>/", views.verify_bus_pass, name="verify_bus_pass"),
]
