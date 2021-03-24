from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm
from .models import Website

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(max_length=32)

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = User(username=username, email=email, password=password)
        user.save()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=32)



class AddWebsiteForm(forms.ModelForm):

    class Meta:
        model = Website
        exclude = ('id', 'user')


class EditWebsiteForm(forms.ModelForm):
    id = forms.UUIDField()
    class Meta:
        model = Website
        exclude = ( 'id','user',)