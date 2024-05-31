from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import re
from django.urls import reverse_lazy
from .forms import *


# Create your views here.
class ProjectListView(generic.ListView):
    model = Project
    context_object_name = 'project_list'
    template_name = 'projects.html'


class ProjectDetailView(generic.DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project.html'


class CustomerDetailView(generic.DetailView):
    model = Customer
    context_object_name = 'customer'
    template_name = 'customer.html'


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    context_object_name = 'customer_list'
    template_name = 'customers.html'


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = 'worker_list'
    template_name = 'workers.html'


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = 'worker'
    template_name = 'worker.html'


# HOME SCREEN
def index(request):
    num_projects = Project.objects.count()
    num_employee = Worker.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {'num_visits': num_visits,
               'num_projects': num_projects,
               'num_employee': num_employee,
               }

    return render(request, 'home.html', context=context)


# SEARCH FIELD
def search(request):
    query_text = request.GET['search_text']
    search_results = Project.objects.filter(Q(name__icontains=query_text) |
                                            Q(place_city__icontains=query_text) |
                                            Q(customer__customer_name__icontains=query_text)
                                            )
    context = {
        'project_list': search_results,
        'query_text': query_text
    }
    return render(request, 'search.html', context=context)


# USER CREATION
@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'registration/registration.html')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.warning(request, "Passwords are not the same")

        if not re.search("\W", password):
            messages.warning(request, "Password should have atleast one symbol")

        if not re.search("\d", password):
            messages.warning(request, "Password should have atleast one number")

        if not re.search("[A-Z]", password):
            messages.warning(request, "Password should have atleast upper case letter")

        if not re.search("[a-z]", password):
            messages.warning(request, "Password should have atleast lower case letter")

        if len(password) < 8:
            messages.warning(request, "Password is not long enough")

        if User.objects.filter(username=username).exists():
            messages.warning(request, f"Profile {username} already exists")

        if not email:
            messages.warning(request, "Enter your email")

        if User.objects.filter(email=email).exists() and email != '':
            messages.warning(request, f"This {email} already have an account. Maybe you forgot password? ")

        if messages.get_messages(request):
            return redirect('register-url')

        User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, f'Your profile: {username}, {email}, successfully registered')
        return redirect('login')


# MY CABINET CREATION
@login_required
def my_cabinet(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.info(request, 'Profile has been updated')
        else:
            messages.warning(request, 'Error has occured')
        return redirect('profile')

    p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'profile.html', context=context)


# def project_create(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         formset = TaskProjectFormSet(request.POST)
#         formset2 = ProjectGroupFormSet(request.POST)
#         if form.is_valid() and formset.is_valid() and formset2.is_valid():
#             project = form.save()
#             project_tasks = formset.save(commit=False)
#             for project_task in project_tasks:
#                 project_task.project = project
#                 project_task.save()
#             return redirect('projects')
#     else:
#         form = ProjectForm()
#         formset = TaskProjectFormSet()
#         formset2 = ProjectGroupFormSet()
#     return render(request, 'assign_workers.html', {
#         'form': form,
#         'formset': formset,
#         'formset2':formset2,
#         })

def assign_workers_to_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    if request.method == 'POST':
        form_group = WorkerGroupForm(request.POST)
        formset_task = WorkerTaskFormset(request.POST)

        if form_group.is_valid() and formset_task.is_valid():
            worker_group = form_group.save(commit=False)
            worker_group.project = project
            worker_group.save()

            worker_tasks = formset_task.save(commit=False)
            for task in worker_tasks:
                task.worker = worker_group.worker
                task.save()

            return redirect('projects')
    else:
        form_group = WorkerGroupForm()
        formset_task = WorkerTaskFormset()

    return render(request, 'assign_workers.html', {
        'form_group': form_group,
        'formset_task': formset_task,
        'project': project,
    })


class UserTaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    # form_class = UserTaskCreateForm, ProjectTaskForm
    template_name = 'task_creation.html'
    success_url = reverse_lazy('success_url_name')

    def get(self, request, *args, **kwargs):
        user_task_form = UserTaskCreateForm()
        project_task_form = ProjectTaskForm()
        return self.render_forms(user_task_form,project_task_form)

    def post(self, request, *args, **kwargs):
        user_task_form = UserTaskCreateForm(request.POST)
        project_task_form = ProjectTaskForm(request.POST)

        if user_task_form.is_valid() and project_task_form.is_valid():
            user_task = user_task_form.save(commit=False)
            user_task.user = request.user
            # user_task.save()
            print(user_task)

            project_task_form = project_task_form.save(commit=False)
            project_task_form.user = user_task
            # project_task_form.save()
            print(project_task_form)

            return redirect(self.success_url)
        return self.render_forms(user_task_form,project_task_form)

    def render_forms(self, user_task_form, project_task_form):
        return render(self.request, self.template_name, {
            'user_task_form': user_task_form,
            'project_task_form': project_task_form,
        })


    # def form_valid(self, form):
    #     # form.instance.reader = self.request.user
    #     form.instance.status = 'ISA'
    #     return super().form_valid(form)