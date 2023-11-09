from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        # fields = UserCreationForm.Meta.fields => username만 불러옴
        fields = ('username', 'profile_image', )