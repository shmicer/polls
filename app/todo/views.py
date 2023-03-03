from .forms import TodoForm, RegisterUserForm, LoginUserForm
from .models import ToDoList, Category

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, CreateView, DeleteView, UpdateView


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
        context['cat_actual_items'] = ToDoList.objects.filter(
            host=self.request.user,
            is_done=False,
            category__slug=self.kwargs['cat_slug']
        )
        context['cat_finished_items'] = ToDoList.objects.filter(
            host=self.request.user,
            is_done=True,
            category__slug=self.kwargs['cat_slug']
        )
        context['title'] = f'ToDo Category {str(self.kwargs["cat_slug"])}'
        return context

    def get_queryset(self):
        return ToDoList.objects.filter(category__slug=self.kwargs['cat_slug'])


class CreateToDoView(CreateView):
    model = ToDoList
    context_object_name = 'todo'
    fields = ['title', 'content', 'due_date']
    success_url = reverse_lazy('view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Item'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.host = self.request.user
        category_name = self.request.POST.get('category')
        form.instance.category = Category.objects.get(name=category_name, slug=category_name)
        return super().form_valid(form)


class UpdateToDoView(UpdateView):
    model = ToDoList
    context_object_name = 'todo'
    fields = ['title', 'content', 'due_date']
    success_url = reverse_lazy('view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Item'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        category_name = self.request.POST.get('category')
        form.instance.category = Category.objects.get(name=category_name, slug=category_name)
        return super().form_valid(form)


class ToDoDeleteView(DeleteView):
    model = ToDoList
    success_url = reverse_lazy('view')


def logout_user(request):
    logout(request)
    return redirect('login')


def mark_as_done(request, pk):
    item = ToDoList.objects.get(id=pk)
    item.is_done = True
    item.save()
    return redirect('view')


