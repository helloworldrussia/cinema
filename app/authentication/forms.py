from django.contrib.auth.forms import UserCreationForm

from authentication.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)
