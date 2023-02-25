from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.logout_user, name='login'),
    path('view', views.todo_ap_view, name='view'),
    path('logout/', views.logout_user, name='logout'),
    path("register/", views.register, name="register"),
    path('add-item/', views.add_todo_view, name='add-item'),
    path('update-item/<int:pk>/', views.update_todo, name='update-item'),
    path('finish/<int:pk>/', views.mark_as_done, name='finish'),
    path('delete-item/<int:pk>/', views.delete_todo, name='delete-item'),

    ]