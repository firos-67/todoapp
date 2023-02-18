import re

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from .models import Task
from .forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView


# Create your views here.


def home(request):
    return render(request, 'home.html')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'index.html'
    fields = ['name', 'date']
    context_object_name = 'tasks'

    def get_queryset(self):
        myset = {
            "finished": Task.objects.filter(user=self.request.user, finished=True).order_by('-updated')[:3],
            "pending": Task.objects.filter(user=self.request.user, finished=False).order_by('date')
        }
        return myset


class TaskDetailsView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'tasks'


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TodoForm
    template_name = 'edit.html'
    context_object_name = 'tasks'

    def get_success_url(self):
        return reverse_lazy('index')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('index')


class MyLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_valid(self, form):
        username=form.cleaned_data['username'].strip()
        password=form.cleaned_data['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(self.request,user)
            return redirect('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(CreateView):
    model = User
    fields = ['username', 'password']
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        cpass = request.POST['cpass']
        msg=self.val_reg(username,password,cpass)
        if msg is None:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')
        else:
            messages.error(request, msg)
            return redirect('register')

    def val_reg(self, username, password, cpass):
        msg = None
        print(cpass,password)
        pattern="^[A-Za-z][A-Za-z0-9]{4,16}$"
        if not re.match(pattern,username):
            msg = "Username should be 5-15 in length & contains only alphabets or numbers"
        elif User.objects.filter(username=username).exists():
            msg = "Username already exists"
        elif cpass != password:
            msg = "Passwords not match"
        elif len(password) < 5 or len(password) >15:
            msg = "password should be 5-15 in length"
        return msg

@login_required()
def add(request):
    if request.method == 'POST':
        name = request.POST.get('name',
                                '')  # request.POST.get() will assign '<value>' (second argument) to the field if no value passed
        # priority=request.POST.get('priority','')  #request.POST.get() only sets values for char or textchar
        date = request.POST.get('date')
        task = Task.objects.create(name=name, date=date, user=request.user)
        task.save()
        return redirect('index')


def finish(request, pk):
    task = Task.objects.get(user=request.user, pk=pk)
    if task is not None:
        task.finished = 'True'
        task.save()
    return redirect('index')


def notfinish(request, pk):
    task = Task.objects.get(user=request.user, pk=pk)
    if task is not None:
        task.finished = 'False'
        task.save()
    return redirect('index')


@login_required()
def logout(request):
    auth.logout(request)
    return redirect('home')
# def index(request):
#     tasks=Task.objects.all()
#     if request.method=='POST':
#         name=request.POST.get('name','')   # request.POST.get() will assign '<value>' (second argument) to the field if no value passed
#         priority=request.POST.get('priority','')  #request.POST.get() only sets values for char or textchar
#         date=request.POST.get('date')
#         task=Task(name=name,priority=priority,date=date)
#         task.save()
#
#     return render(request,'index.html',{'tasks':tasks})

# def delete(request,task_id):
#     if request.method=='POST':
#         task=Task.objects.get(id=task_id)
#         task.delete()
#         return redirect('/')
#     return render(request,'delete.html')
#
# def update(request,id):
#     task=Task.objects.get(id=id)
#     form=TodoForm(request.POST or None, instance=task)
#     if form.is_valid():
#         form.save()
#         return redirect('/')
#     return render(request,'update.html',{'form':form,'task':task})
