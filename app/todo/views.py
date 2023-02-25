from django.shortcuts import render, redirect
from .models import ToDoList, Category, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import TodoForm, UserRegistrationForm


def home(request):
    return render(request, 'todo/base.html')


def loginUser(request):
    return render(request, 'todo/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def register(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('view')
    else:
        messages.error(request, 'An error occurred')
    return render(request, 'todo/register.html', {'form': form})


def todoappView(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    todo_items = ToDoList.objects.filter(Q(category__name__contains=q), host=request.user)
    categories = Category.objects.all()
    return render(request, 'todo/home.html', {'all_items': todo_items, 'categories': categories})


@login_required(login_url='login')
def addTodoView(request):
    form = TodoForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.host = request.user
            form.save()
            return redirect('view')
    else:
        messages.error(request, 'An error occurred')
    context = {'form': form, 'categories': categories}
    return render(request, 'todo/todo_form.html', context)


def updateTodo(request, pk):
    update_todo = ToDoList.objects.get(id=pk)
    form = TodoForm(instance=update_todo)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=update_todo)
        if form.is_valid():
            form.save()
            return redirect('view')
    context = {'form': form, }
    return render(request, 'todo/todo_form.html', context)


def deleteTodo(request, pk):
    delete_item = ToDoList.objects.get(id=pk)
    delete_item.delete()
    return redirect('view')

