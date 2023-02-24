from django.forms import ModelForm
from .models import ToDoList, Category
from django.contrib.auth.forms import UserCreationForm


class TodoForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = '__all__'