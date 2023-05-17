from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

class AddAlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['description', ]
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-input'}),
        }


class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', ]
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-input'}),
        }

class AddPhotoForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['album', 'location', 'title', 'description', 'img']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.TextInput(attrs={'class': 'form-input'}),
        }



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

