from django.contrib import admin
from .models import ToDoList, Category

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Category)