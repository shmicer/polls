from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class ToDoList(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250, default='Title', null=False)
    content = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)
    due_date = models.DateField(default=timezone.now().strftime('%Y-%m-%d'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

