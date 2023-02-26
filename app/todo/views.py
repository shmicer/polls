from django.shortcuts import render, redirect
from .models import ToDoList, Category, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import TodoForm, UserRegistrationForm


def home(request):
    return render(request, 'todo/base.html')


def login_user(request):
    return render(request, 'todo/login.html')


def logout_user(request):
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


def todo_ap_view(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    todo_items = ToDoList.objects.filter(Q(category__name__contains=q), host=request.user, is_done=False)
    finished_items = ToDoList.objects.filter(Q(category__name__contains=q), host=request.user, is_done=True)
    categories = Category.objects.all()
    return render(request, 'todo/home.html', {'actual_items': todo_items, 'finished_items': finished_items, 'categories': categories})


@login_required(login_url='login')
def add_todo_view(request):
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


def update_todo(request, pk):
    todo = ToDoList.objects.get(id=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        todo.title = request.POST.get('title')
        todo.content = request.POST.get('content')
        todo.due_date = request.POST.get('due_date')
        category.name = request.POST.get('category')
        todo.save()
        return redirect('view')
    context = {'categories': categories, 'todo': todo}
    return render(request, 'todo/todo_form.html', context)


def delete_todo(request, pk):
    delete_item = ToDoList.objects.get(id=pk)
    delete_item.delete()
    return redirect('view')


def mark_as_done(request, pk):
    item = ToDoList.objects.get(id=pk)
    item.is_done = True
    item.save()
    return redirect('view')
