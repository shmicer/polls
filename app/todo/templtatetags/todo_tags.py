from django import template
from todo.models import Category

register = template.Library()


@register.inclusion_tag('todo/categories_component.html')
def show_categories():
    cats = Category.objects.all()
    return {"cats": cats}


