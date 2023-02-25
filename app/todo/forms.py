from django.forms import ModelForm
from .models import ToDoList, Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TodoForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ('title', 'category', 'content', 'due_date')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')