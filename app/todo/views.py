from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import ToDoList, Category
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView

from .forms import TodoForm, RegisterUserForm, LoginUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'todo/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('view')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'todo/login.html'


def logout_user(request):
    logout(request)
    return redirect('login')


class TodoAppView(ListView):
    model = ToDoList
    context_object_name = 'actual_items'
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['finished_items'] = ToDoList.objects.filter(is_done=True)
        context['title'] = 'ToDo List'
        context['categories'] = Category.objects.all()
        return context


class CategoryView(ListView):
    model = ToDoList
    context_object_name = 'actual_items'
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"ToDo Category - {str(context['actual_items'][0].category)}"
        return context

    def get_queryset(self):
        return ToDoList.objects.filter(category__slug=self.kwargs['cat_slug'])


def add_todo_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TodoForm()
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name, slug=category_name)
        ToDoList.objects.create(
            host=request.user,
            title=request.POST.get('title'),
            category=category,
            content=request.POST.get('content'),
            due_date=request.POST.get('due_date')
        )
        return redirect('view')
    else:
        form = TodoForm()
    context = {'form': form, 'categories': categories}
    return render(request, 'todo/todo_form.html', context)


def update_todo(request, pk):
    todo = ToDoList.objects.get(id=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        ToDoList.objects.update(
            title=request.POST.get('title'),
            category=category,
            content=request.POST.get('content'),
            due_date=request.POST.get('due_date')
        )
        return redirect('view')
    context = {'categories': categories, 'todo': todo}
    return render(request, 'todo/todo_form.html', context)


def mark_as_done(request, pk):
    item = ToDoList.objects.get(id=pk)
    item.is_done = True
    item.save()
    return redirect('view')


def delete_todo(request, pk):
    delete_item = ToDoList.objects.get(id=pk)
    delete_item.delete()
    return redirect('view')
