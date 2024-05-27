from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator
from .models import User


class CreateUserForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("First name")
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label=_("Last name")
    )

    username = forms.CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=_("Required field. No more than 150 characters. Only letters, numbers and @.+-_ characters.") # noqa e501
            )
        ],
        help_text=_("Required field. No more than 150 characters. Only letters, numbers and @.+-_ characters.") # noqa e501
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'password1', 'password2')
