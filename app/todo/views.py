from django.shortcuts import render, redirect
from .models import ToDoList, Category
from django.db.models import Q
from .forms import TodoForm


def todoappView(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    todo_items = ToDoList.objects.filter(Q(category__name__contains=q)
    categories = Category.objects.all()
    return render(request, 'todo/todolist.html', {'all_items': todo_items, 'categories': categories})


def addTodoView(request):
    form = TodoForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    context = {'form': form, 'categories': categories}
    return render(request, 'todo/todo_form.html', context)


def updateTodo(request, pk):
    update_todo = ToDoList.objects.get(id=pk)
    form = TodoForm(instance=update_todo)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=update_todo)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    context = {'form': form, }
    return render(request, 'todo/todo_form.html', context)


def deleteTodo(request, pk):
    delete_item = ToDoList.objects.get(id=pk)
    delete_item.delete()
    return redirect('/todo')

