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
    return redirect('login')


def register(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
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
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        ToDoList.objects.create(
            host=request.user,
            title=request.POST.get('title'),
            category=category,
            content=request.POST.get('content'),
            due_date=request.POST.get('due_date')
        )
        return redirect('view')
    else:
        messages.error(request, 'An error occurred')
    context = {'form': form, 'categories': categories}
    return render(request, 'todo/todo_form.html', context)


def updateTodo(request, pk):
    todo = ToDoList.objects.get(id=pk)
    form = TodoForm(instance=todo)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        todo.title = request.POST.get('title')
        todo.content = request.POST.get('content')
        todo.due_date = request.POST.get('due_date')
        category.name = request.POST.get('category')
        todo.save()
        return redirect('view')
    context = {'form': form, 'categories': categories}
    return render(request, 'todo/todo_form.html', context)


def deleteTodo(request, pk):
    delete_item = ToDoList.objects.get(id=pk)
    delete_item.delete()
    return redirect('view')

