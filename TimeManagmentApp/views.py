from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import re
from django.urls import reverse_lazy
from .forms import *


class ProjectDetailView(generic.DetailView):
    """
    Project detalized view for one project
    """
    model = Project
    context_object_name = 'project'
    template_name = 'detailed_templates/project.html'


class ProjectListView(generic.ListView):
    """
    Project list view for all projects
    """
    model = Project
    context_object_name = 'project_list'
    template_name = 'list_templates/projects.html'


class UserProjectCreateView(LoginRequiredMixin, generic.CreateView):
    """
    User project form creation view
    With info messaging
    """
    model = Project
    template_name = 'creation/project_creation.html'
    form_class = ProjectForm
    success_url = reverse_lazy('add-project')

    def form_valid(self, form):
        messages.info(self.request, 'Project has been added')
        return super().form_valid(form)


class UserProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
     User project form update view
    With info messaging
    """
    model = Project
    form_class = ProjectPictureUpdateForm
    template_name = 'updation/project_updation.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        messages.info(self.request, f'{self.object.name} project has been updated')
        return super().form_valid(form)


class CustomerDetailView(generic.DetailView):
    """
    Customer detalized view for one customer
    """
    model = Customer
    context_object_name = 'customer'
    template_name = 'detailed_templates/customer.html'


class CustomerListView(LoginRequiredMixin, generic.ListView):
    """
    Customer list view for all customers
    """
    model = Customer
    context_object_name = 'customer_list'
    template_name = 'list_templates/customers.html'


class UserCustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Customer update view
    """
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'updation/customer_updation.html'
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        messages.info(self.request, f'{self.object.customer_name} information has been updated')
        return super().form_valid(form)


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Worker detalized view for one worker
    """
    model = Worker
    context_object_name = 'worker'
    template_name = 'detailed_templates/worker.html'


class WorkerListView(LoginRequiredMixin, generic.ListView):
    """
    Worker list view for all workers
    """
    model = Worker
    context_object_name = 'worker_list'
    template_name = 'list_templates/workers.html'


class UserWorkerCreateView(LoginRequiredMixin, generic.CreateView):
    """
    User worker creation view
    With info messaging
    """
    model = Worker
    template_name = 'creation/worker_creation.html'
    form_class = UserWorkerCreateForm
    success_url = reverse_lazy('add-worker')

    def form_valid(self, form):
        messages.info(self.request, 'Worker has been created')
        return super().form_valid(form)


class UserWorkerGroupCreateView(LoginRequiredMixin, generic.CreateView):
    """
    User Workergroup creation view

    """
    template_name = 'creation/assign_workers.html'
    success_url = reverse_lazy('assign-groups')

    def get(self, request, *args, **kwargs):
        """
        Overwriting Get method to combine 2 forms
        """
        worker_group_form = WorkerGroupForm()
        worker_task_form = WorkerTaskForm()
        return self.render_forms(worker_group_form, worker_task_form)

    def post(self, request, *args, **kwargs):
        """
        Using commit=False to delay commiting to database
        """
        worker_group_form = WorkerGroupForm(request.POST)
        worker_task_form = WorkerTaskForm(request.POST)

        if worker_group_form.is_valid() and worker_task_form.is_valid():
            worker_group = worker_group_form.save(commit=False)
            worker_group.user = request.user
            worker_group.save()

            worker_task = worker_task_form.save(commit=False)
            worker_task.worker_group = worker_group
            worker_task.worker_id = worker_group.worker.id
            worker_task.save()

            messages.info(self.request, 'Group has been assigned')
            return redirect(self.success_url)
        return self.render_forms(worker_group_form, worker_task_form)

    def render_forms(self, worker_group_form, worker_task_form):
        """
        Form rendering
        """
        return render(self.request, self.template_name, {
            'worker_group_form': worker_group_form,
            'worker_task_form': worker_task_form,
        })


class UserWorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    User worker form updating
    """
    model = Worker
    form_class = WorkerUpdateForm
    template_name = 'updation/worker_updation.html'
    success_url = reverse_lazy('workers')

    def get(self, request, *args, **kwargs):
        """
        Overwriting Get method to combine 2 forms
        """
        worker_update_form = WorkerUpdateForm(instance=self.get_object())
        user_form = UserGroupUpdateForm()
        return self.render_forms(worker_update_form, user_form)

    def post(self, request, *args, **kwargs):
        """
        Overwriting post method to save params
        """
        worker_update_form = WorkerUpdateForm(request.POST, instance=self.get_object())
        user_form = UserUpdateForm(request.POST, instance=request.user.groups)

        if worker_update_form.is_valid() and user_form.is_valid():
            worker_update_form.save()
            user_form.save()

            messages.info(self.request, 'Group has been assigned')
            return redirect(self.success_url)
        return self.render_forms(worker_update_form, user_form)

    def render_forms(self, worker_update_form, user_form):
        """
        form rendering
        """
        return render(self.request, self.template_name, {
            'worker_update_form': worker_update_form,
            'user_form': user_form,
        })

    def form_valid(self, form):
        """
        Messaging about success
        """
        messages.info(self.request, f'{self.object.user} information has been updated')
        return super().form_valid(form)


class VehicleListView(LoginRequiredMixin, generic.ListView):
    """
    Vehicle detalized view for one vehicle
    """

    model = Vehicle
    context_object_name = 'vehicles_list'
    template_name = 'list_templates/vehicles.html'


class VehicleDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Vehiclle list view for all vehicles
    """
    model = Vehicle
    context_object_name = 'vehicle'
    template_name = 'detailed_templates/vehicle.html'


class UserVehicleCreateView(LoginRequiredMixin, generic.CreateView):
    """
    User vehicle creation view
    With info messaging
    """
    model = Vehicle
    template_name = 'creation/vehicle_creation.html'
    form_class = UserVehicleCreateForm
    success_url = reverse_lazy('add-vehicle')

    def form_valid(self, form):
        messages.info(self.request, 'Car has been added')
        return super().form_valid(form)


class UserVehicleUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    User vehicle update view
    With info messaging
    """
    model = Vehicle
    form_class = UserVehicleCreateForm
    template_name = 'updation/vehicle_updation.html'
    success_url = reverse_lazy('vehicles')

    def form_valid(self, form):
        messages.info(self.request, f'{self.object.license_plate} information has been updated')
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, generic.ListView):
    """
    Task list view for all tasks
    """
    model = Task
    context_object_name = 'task_list'
    template_name = 'list_templates/tasks.html'

    def get_queryset(self):
        """
        Return query set of task objects ordered by priority 0-5
        Also for group Worker returns all assigned to him tasks
        :return:order by priority 0-5
        """
        user = self.request.user
        if user.groups.filter(name='worker').exists():
            worker = Worker.objects.get(user=user)
            worker_tasks = WorkerTask.objects.filter(worker=worker).values_list('task_id', flat=True)
            if worker_tasks.exists():
                return Task.objects.filter(id__in=worker_tasks).order_by('priority')
            else:
                return Task.objects.none()  #
        else:
            return Task.objects.order_by('priority')


@login_required
def change_task_status(request, task_id, new_status):
    """
    Task status can be changed with a button
    """
    user = request.user
    worker = get_object_or_404(Worker, user=user)
    task = get_object_or_404(Task, id=task_id)

    if WorkerTask.objects.filter(worker=worker, task=task).exists():
        task.status = new_status
        task.save()
        return redirect('tasks')
    else:
        return redirect('tasks')


class TasksDetailView(LoginRequiredMixin, generic.DetailView, generic.edit.FormMixin, ):
    """
    Task detalized view for one Task
    """
    model = Task
    context_object_name = 'task'
    template_name = 'detailed_templates/task.html'
    form_class = TaskReviewForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TaskReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('task', kwargs={'pk': self.object.pk})


class UserTaskCreateView(LoginRequiredMixin, generic.CreateView):
    """
    User task creation view

    """
    model = Task
    template_name = 'creation/task_creation.html'
    success_url = reverse_lazy('add-task')

    def get(self, request, *args, **kwargs):
        """
        Overwriting Get method to combine 2 forms
        """
        user_task_form = UserTaskCreateForm()
        project_task_form = ProjectTaskForm()
        return self.render_forms(user_task_form, project_task_form)

    def post(self, request, *args, **kwargs):
        """
         Using commit=False to delay commiting to database
        """
        user_task_form = UserTaskCreateForm(request.POST)
        project_task_form = ProjectTaskForm(request.POST)

        if user_task_form.is_valid() and project_task_form.is_valid():
            user_task = user_task_form.save(commit=False)
            user_task.user = request.user
            user_task.save()

            project_task_form = project_task_form.save(commit=False)
            project_task_form.task = user_task
            project_task_form.save()

            messages.info(self.request, 'Task has been created')
            return redirect(self.success_url)
        return self.render_forms(user_task_form, project_task_form)

    def render_forms(self, user_task_form, project_task_form):
        """
        Form rendering
        """
        return render(self.request, self.template_name, {
            'user_task_form': user_task_form,
            'project_task_form': project_task_form,
        })


class UserTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Task delete view
    """
    model = Task
    template_name = 'deletion/task_deletion.html'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Worker delete view from user side
    """
    model = Worker
    template_name = 'deletion/worker_deletion.html'
    success_url = reverse_lazy('workers')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class UserTaskManager(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = WorkerTask
    form_class = ManagerWorkerTaskForm
    template_name = 'taskmanager.html'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


class TaskManagementView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        WorkerTaskFormSet = inlineformset_factory(Task, WorkerTask, fields=('worker',), extra=1)
        formset = WorkerTaskFormSet(instance=task)
        return render(request, 'task_management.html', {'task': task, 'formset': formset})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        WorkerTaskFormSet = inlineformset_factory(Task, WorkerTask, fields=('worker',),
                                                  extra=1)
        formset = WorkerTaskFormSet(request.POST, instance=task)
        if formset.is_valid():
            formset.save()
            messages.info(self.request, f'Information has been updated')
            return redirect('tasks')
        return render(request, 'task_management.html', {'task': task, 'formset': formset})

    def test_func(self):
        return self.request.user.groups.filter(name='manager').exists()


def index(request):
    """
    Greeting page, show main information about size of the company

    """
    num_projects = Project.objects.count()
    num_employee = Worker.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {'num_visits': num_visits,
               'num_projects': num_projects,
               'num_employee': num_employee,
               }

    return render(request, 'home.html', context=context)


def search(request):
    """
    Search view able to search by name of the project, city and customer

    """
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
    """
    Registration view with password difficulty,
    after creation adds to worker group
     """
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

        User.objects.create_user(username=username, email=email, password=password).groups.add(Group.objects.get(id=2))
        messages.info(request, f'Your profile: {username}, {email}, successfully registered')
        return redirect('login')


@login_required
def my_cabinet(request):
    """

    Personal user cabinet creation view

    """
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
