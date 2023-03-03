from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .models import ToDoList, Category
from django.contrib.auth import logout, login
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class TodoAppView(LoginRequiredMixin, ListView):
    model = ToDoList
    context_object_name = 'items'
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_actual_items'] = ToDoList.objects.filter(host=self.request.user, is_done=False)
        context['cat_finished_items'] = ToDoList.objects.filter(host=self.request.user, is_done=True)
        context['title'] = 'ToDo List'
        context['categories'] = Category.objects.all()
        return context


class CategoryView(LoginRequiredMixin, ListView):
    model = ToDoList
    context_object_name = 'items'
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cat_actual_items'] = ToDoList.objects.filter(host=self.request.user, is_done=False, category__slug=self.kwargs['cat_slug'])
        context['cat_finished_items'] = ToDoList.objects.filter(host=self.request.user, is_done=True, category__slug=self.kwargs['cat_slug'])
        context['title'] = f'ToDo Category {str(self.kwargs["cat_slug"])}'
        return context

    def get_queryset(self):
        cat_items = ToDoList.objects.filter(category__slug=self.kwargs['cat_slug'])
        return cat_items


def add_todo_view(request):
    categories = Category.objects.all()
    title = 'Create ToDo'
    form = TodoForm()
    if request.method == 'POST':
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
    context = {'form': form, 'categories': categories, 'title': title}
    return render(request, 'todo/todo_form.html', context)


def update_todo(request, pk):
    todo = ToDoList.objects.get(id=pk)
    title = 'Update ToDo'
    categories = Category.objects.all()
    form = TodoForm(instance=todo)
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        todo.title = request.POST.get('title')
        todo.category = category
        todo.content = request.POST.get('content')
        todo.due_date = request.POST.get('due_date')
        todo.save()
        return redirect('view')
    else:
        form = TodoForm()
    context = {'categories': categories, 'todo': todo, 'form': form, 'title': title}
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
