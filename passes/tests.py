
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BusPassApplication, DigitalBusPass


class BusPassSystemTests(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username="student1",
            password="TestPassword123!"
        )

        self.other_student = User.objects.create_user(
            username="student2",
            password="TestPassword123!"
        )

        self.application = BusPassApplication.objects.create(
            student=self.student,
            date_of_birth=date(2004, 5, 10),
            college_name="GM Institute of Technology",
            course="AIML",
            address="Davangere",
            source="Davangere",
            destination="Dharwad",
            status="APPROVED",
        )

        self.digital_pass = DigitalBusPass.objects.create(
            application=self.application,
            pass_number="BUS-TEST123",
            valid_until=date.today() + timedelta(days=30),
        )

    def test_my_applications_requires_login(self):
        response = self.client.get(
            reverse("my_applications")
        )
        self.assertEqual(response.status_code, 302)

    def test_student_sees_only_own_applications(self):
        self.client.login(
            username="student1",
            password="TestPassword123!"
        )

        response = self.client.get(
            reverse("my_applications")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "GM Institute of Technology"
        )

    def test_student_can_view_own_digital_pass(self):
        self.client.login(
            username="student1",
            password="TestPassword123!"
        )

        response = self.client.get(
            reverse("my_digital_pass")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BUS-TEST123")

    def test_valid_pass_verification(self):
        response = self.client.get(
            reverse(
                "verify_bus_pass",
                kwargs={"pass_number": "BUS-TEST123"}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_valid"])

    def test_expired_pass_is_invalid(self):
        self.digital_pass.valid_until = (
            date.today() - timedelta(days=1)
        )
        self.digital_pass.save()

        response = self.client.get(
            reverse(
                "verify_bus_pass",
                kwargs={"pass_number": "BUS-TEST123"}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_valid"])

    def test_unknown_pass_is_invalid(self):
        response = self.client.get(
            reverse(
                "verify_bus_pass",
                kwargs={"pass_number": "BUS-UNKNOWN"}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_valid"])

    def test_new_application_is_pending_by_default(self):
        application = BusPassApplication.objects.create(
            student=self.student,
            date_of_birth=date(2004, 5, 10),
            college_name="Test College",
            course="AIML",
            address="Davangere",
            source="Davangere",
            destination="Dharwad",
        )

        self.assertEqual(application.status, "PENDING")
        self.assertFalse(
            DigitalBusPass.objects.filter(
                application=application
            ).exists()
        )
