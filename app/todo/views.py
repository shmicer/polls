from django.shortcuts import render, redirect
from .models import ToDoList, Category
from django.db.models import Q
from .forms import TodoForm


def todoappView(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    todo_items = ToDoList.objects.filter(Q(category__name__icontains=q) |
                                Q(title__icontains=q) |
                                Q(content__icontains=q)
                                )
    categories = Category.objects.all()
    todo_count = todo_items.count()
    return render(request, 'todo/todolist.html', {'all_items': todo_items, 'todo_count': todo_count, 'categories': categories})


def addTodoView(request):
    form = TodoForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        ToDoList.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            category=category,
            due_date=request.POST.get('due_date'),
        )
        return redirect('todolist')
    context = {'form': form, 'categories': categories}
    return render(request, 'todo/todo_form.html', context)


def deleteTodo(request, pk):
    delete_item = ToDoList.objects.get(id=pk)
    delete_item.delete()
    return redirect('/todo')

