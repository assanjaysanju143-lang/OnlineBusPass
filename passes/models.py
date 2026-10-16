
from django.db import models
from django.contrib.auth.models import User


class BusPassApplication(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bus_pass_applications",
    )

    date_of_birth = models.DateField()
    college_name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    address = models.TextField()

    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.source} to {self.destination}"


class DigitalBusPass(models.Model):
    application = models.OneToOneField(
        BusPassApplication,
        on_delete=models.CASCADE,
        related_name="digital_pass",
    )

    pass_number = models.CharField(
        max_length=30,
        unique=True,
    )

    issued_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField()

    def __str__(self):
        return self.pass_number
