from django.contrib.auth.forms import UserCreationForm
from .models import ClientModel
from django import forms
from django.utils.translation import gettext_lazy as _


class CreateClientForm(UserCreationForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = ClientModel
        fields = ("username", "email", "first_name", "last_name", "is_company")
