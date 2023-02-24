from django.urls import path
from . import views

urlpatterns = [
    path('', views.todoappView, name='todolist'),
    path('add-item/', views.addTodoView, name='add-item'),
    path('update-item/<int:pk>/', views.updateTodo, name='update-item'),
    path('delete-item/<int:pk>/', views.deleteTodo, name='delete-item'),

    ]