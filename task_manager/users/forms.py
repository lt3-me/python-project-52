from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserDataForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'first_name', 'last_name', 'username',
            'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        return username
