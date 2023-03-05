from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path('view', views.TodoAppView.as_view(), name='view'),
    path('add-item/', views.CreateToDoView.as_view(), name='add-item'),
    path('update-item/<int:pk>/', views.UpdateToDoView.as_view(), name='update-item'),
    path('<int:pk>/delete', views.ToDoDeleteView.as_view(), name='delete-item'),
    path('<slug:cat_slug>/', views.TodoAppView.as_view(), name='category'),
    path('finish/<int:pk>/', views.mark_as_done, name='finish'),
    path('__debug__/', include('debug_toolbar.urls')),
    ]
