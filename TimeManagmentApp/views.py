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

from .models import *


# Create your views here.
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
            messages.warning(request, "Slaptazodziai nesutampa!!")

        if User.objects.filter(username=username).exists():
            messages.warning(request, f"Profilis {username} jau uzimtas")

        if not email:
            messages.warning(request, "Email ne ivestas")

        if User.objects.filter(email=email).exists():
            messages.warning(request, f"Pastas {email} jau uzimtas. Gal pamirsote slaptazodi?")

        # jeigu yra nor viena zinute messages(reiskia turime klada ir neimanoma iregisstruoti vartotoja)
        if messages.get_messages(request):
            return redirect('register-url')

        # jeigu nebuvo kurimo metu jokiu klaidu mes galime registruoti nauja useri
        User.objects.create_user(username=username, email=email, password=password)
        messages.info(request, f'Jusu profilis: {username}, {email}, sekmingai uregistruotas')
        return redirect('login')