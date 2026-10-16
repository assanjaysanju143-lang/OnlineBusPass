
from django import forms
from .models import BusPassApplication


class BusPassApplicationForm(forms.ModelForm):
    class Meta:
        model = BusPassApplication

        fields = [
            "date_of_birth",
            "college_name",
            "course",
            "address",
            "source",
            "destination",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "college_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "course": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "source": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "destination": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }
