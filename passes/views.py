
from io import BytesIO
import base64

import qrcode

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import BusPassApplicationForm
from .models import BusPassApplication, DigitalBusPass


@login_required(login_url="login")
def apply_for_pass(request):
    if request.method == "POST":
        form = BusPassApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.save()

            messages.success(
                request,
                "Your bus pass application was submitted successfully!",
            )

            return render(
                request,
                "apply_for_pass.html",
                {
                    "form": BusPassApplicationForm(),
                    "submitted": True,
                },
            )
    else:
        form = BusPassApplicationForm()

    return render(
        request,
        "apply_for_pass.html",
        {"form": form},
    )


@login_required(login_url="login")
def my_applications(request):
    applications = BusPassApplication.objects.filter(
        student=request.user
    ).order_by("-applied_at")

    return render(
        request,
        "my_applications.html",
        {"applications": applications},
    )


@login_required(login_url="login")
def student_dashboard(request):
    applications = BusPassApplication.objects.filter(
        student=request.user
    )

    context = {
        "total_applications": applications.count(),
        "pending_count": applications.filter(status="PENDING").count(),
        "approved_count": applications.filter(status="APPROVED").count(),
        "rejected_count": applications.filter(status="REJECTED").count(),
    }

    return render(
        request,
        "student_dashboard.html",
        context,
    )


@login_required(login_url="login")
def my_digital_pass(request):
    digital_passes = DigitalBusPass.objects.filter(
        application__student=request.user,
        application__status="APPROVED",
    ).select_related(
        "application",
        "application__student",
    ).order_by("-issued_at")

    for digital_pass in digital_passes:
        verification_url = request.build_absolute_uri(
            f"/passes/verify/{digital_pass.pass_number}/"
        )

        qr = qrcode.make(verification_url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        digital_pass.qr_code_base64 = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    return render(
        request,
        "my_digital_pass.html",
        {"digital_passes": digital_passes},
    )


def verify_bus_pass(request, pass_number):
    digital_pass = (
        DigitalBusPass.objects
        .select_related("application", "application__student")
        .filter(pass_number=pass_number)
        .first()
    )

    is_valid = (
        digital_pass is not None
        and digital_pass.application.status == "APPROVED"
        and digital_pass.valid_until >= timezone.localdate()
    )

    return render(
        request,
        "verify_bus_pass.html",
        {
            "digital_pass": digital_pass,
            "is_valid": is_valid,
        },
    )
