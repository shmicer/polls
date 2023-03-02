from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import ToDoList
from django import forms
from django.contrib.auth.models import User


class TodoForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ('title', 'category', 'content', 'due_date')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat password')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))