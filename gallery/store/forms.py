from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import profile
from django.forms.models import ModelForm

from django.forms.widgets import FileInput


class CreateUserForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_img': FileInput(),
        }
        
#Customer.objects.create(User = request.user)