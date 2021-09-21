from django.forms import forms, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Host


class ExtendedUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=True)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class HostCreationForm(ModelForm):
    class Meta:
        model = Host
        fields = ('nationality', 'first_language', 'location')

        
        




