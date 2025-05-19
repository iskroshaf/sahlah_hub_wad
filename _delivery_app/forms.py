
from django import forms
from .models import DeliveryMethod

class DeliveryMethodForm(forms.ModelForm):
    class Meta:
        model  = DeliveryMethod
        fields = [
            "code",
            "name",
            "desc",
            "base_price",
            "est_day_min",
            "est_day_max",
            "is_active",
        ]
        widgets = {
            "code":        forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. fast"}),
            "name":        forms.TextInput(attrs={"class": "form-control", "placeholder": "Fast Delivery"}),
            "desc":        forms.Textarea(attrs={"class": "form-control", "style": "height: 100px"}),
            "base_price":  forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "est_day_min": forms.NumberInput(attrs={"class": "form-control"}),
            "est_day_max": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active":   forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "code":        "Unique Code",
            "name":        "Display Name",
            "desc":        "Description",
            "base_price":  "Base Price (RM)",
            "est_day_min": "ETA Min (days)",
            "est_day_max": "ETA Max (days)",
            "is_active":   "Active?",
        }