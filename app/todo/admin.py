from django.contrib import admin
from .models import ToDoList, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ToDoList)
admin.site.register(Category, CategoryAdmin)


