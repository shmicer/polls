from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.logoutUser, name='login'),
    path('view', views.todoappView, name='view'),
    path('logout/', views.logoutUser, name='logout'),
    path("register/", views.register, name="register"),
    path('add-item/', views.addTodoView, name='add-item'),
    path('update-item/<int:pk>/', views.updateTodo, name='update-item'),
    path('delete-item/<int:pk>/', views.deleteTodo, name='delete-item'),

    ]