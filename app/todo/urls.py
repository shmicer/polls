from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path('view', views.TodoAppView.as_view(), name='view'),
    path('add-item/', views.add_todo_view, name='add-item'),
    path('update-item/<int:pk>/', views.update_todo, name='update-item'),
    path('finish/<int:pk>/', views.mark_as_done, name='finish'),
    path('delete-item/<int:pk>/', views.delete_todo, name='delete-item'),
    path('<slug:cat_slug>', views.CategoryView.as_view(), name='category'),
    ]