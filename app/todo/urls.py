from django.urls import path
from . import views

urlpatterns = [
    path('', views.todoappView, name='todolist'),
    path('addItem/', views.addTodoView, name='addItem'),
    path('deleteItem/<int:pk>/', views.deleteTodo, name='deleteItem'),

    ]