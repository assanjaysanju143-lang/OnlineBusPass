
from datetime import date, timedelta
from uuid import uuid4

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import BusPassApplication, DigitalBusPass


@admin.register(BusPassApplication)
class BusPassApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "college_name",
        "source",
        "destination",
        "status",
        "applied_at",
    )

    list_filter = ("status", "applied_at")

    search_fields = (
        "student__username",
        "college_name",
        "source",
        "destination",
    )

    list_editable = ("status",)
    ordering = ("-applied_at",)

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            super().save_model(request, obj, form, change)

            if obj.status == "APPROVED":
                DigitalBusPass.objects.get_or_create(
                    application=obj,
                    defaults={
                        "pass_number": f"BUS-{uuid4().hex[:12].upper()}",
                        "valid_until": date.today() + timedelta(days=365),
                    },
                )


@admin.register(DigitalBusPass)
class DigitalBusPassAdmin(admin.ModelAdmin):
    list_display = (
        "pass_number",
        "application",
        "issued_at",
        "valid_until",
    )

    search_fields = (
        "pass_number",
        "application__student__username",
    )

    ordering = ("-issued_at",)

    def has_add_permission(self, request):
        return False
