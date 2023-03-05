from .forms import RegisterUserForm, LoginUserForm
from .utils import *

from django.shortcuts import redirect, get_object_or_404
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
    context_object_name = 'items'
    template_name = 'todo/login.html'


class TodoAppView(LoginRequiredMixin, ListView):
    model = ToDoList
    context_object_name = 'items'
    template_name = 'todo/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = 'ToDo List'
        context['items'] = context['items'].filter(host=self.request.user).select_related('category')
        if 'cat_slug' in self.kwargs:
            self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
            context['items'] = context['items'].filter(category=self.category)
        context['actual'] = len(context['items'].filter(is_done=False))
        context['finished'] = len(context['items']) - context['actual']
        return context


class CreateToDoView(LoginRequiredMixin, DataMixin, CreateView):
    model = ToDoList
    context_object_name = 'todo'
    fields = ['title', 'content', 'due_date']
    success_url = reverse_lazy('view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add Item')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        form.instance.host = self.request.user
        category_name = self.request.POST.get('category')
        form.instance.category = Category.objects.get(name=category_name, slug=category_name)
        return super().form_valid(form)


class UpdateToDoView(LoginRequiredMixin, DataMixin, UpdateView):
    model = ToDoList
    context_object_name = 'todo'
    fields = ['title', 'content', 'due_date']
    success_url = reverse_lazy('view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Edit Item')
        context = dict(list(context.items()) + list(c_def.items()))
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


