from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls_base.urls')),
    path('todo/', include('todo.urls')),
    path('admin/', admin.site.urls),
]
