from django import forms
from django.forms.models import inlineformset_factory
from .models import *
from django.db.models import Q


class DateTimeInput(forms.DateTimeInput):
    """
    Date time form to change time and date
    """
    input_type = 'datetime-local'


class DateInput(forms.DateInput):
    """
    Date  form to change  date
    """
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
    """
    Form used in profile picture update
    """

    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    """
    Form used in user information update
    """

    class Meta:
        model = User
        fields = ('email',)


class UserGroupUpdateForm(forms.ModelForm):
    """
    Form used for user group update
    """

    class Meta:
        model = User
        fields = ('groups',)


class WorkerGroupForm(forms.ModelForm):
    """
    Form used in worker group creation
    """

    class Meta:
        model = WorkerGroup
        fields = ('project', 'vehicle', 'worker')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worker'].queryset = Worker.objects.exclude(
            Q(workergroup__isnull=False) | Q(status__icontains='NOT'))


class WorkerTaskForm(forms.ModelForm):
    """
    Form used for assigning tasks to a worker
    """

    class Meta:
        model = WorkerTask
        fields = ('task',)


class ManagerWorkerTaskForm(forms.ModelForm):
    """
    Same as previous but for managaer
    """

    class Meta:
        model = WorkerTask
        fields = ('worker', 'task')


class ProjectTaskForm(forms.ModelForm):
    """
    Form for task assignment for a project
    """

    class Meta:
        model = ProjectTask
        fields = ('project',)


class ProjectForm(forms.ModelForm):
    """
    project creation form
    """

    class Meta:
        model = Project
        fields = ['name', 'description', 'place_city', 'customer', 'project_start', 'project_end']
        widgets = {
            'project_start': DateInput(),
            'project_end': DateInput(),
        }


class WorkerFilterForm(forms.Form):
    """
    Worker filter form
    """
    status = forms.CharField(required=False, label='Status')
    date_joined = forms.DateField(required=False, label='Date Joined',
                                  widget=forms.DateInput(attrs={'type': 'date'}))


class ProjectPictureUpdateForm(forms.ModelForm):
    """
    Project update form
    """

    class Meta:
        model = Project
        fields = ['name', 'description', 'place_city', 'customer', 'project_start', 'project_end', 'picture']
        widgets = {
            'project_start': DateInput(),
            'project_end': DateInput(),
        }


class CustomerUpdateForm(forms.ModelForm):
    """
    Customer update form
    """

    class Meta:
        model = Customer
        fields = '__all__'


class WorkerUpdateForm(forms.ModelForm):
    """
    Worker update form
    """

    class Meta:
        model = Worker
        fields = '__all__'
        widgets = {
            'availability_date': DateInput()
        }


class UserTaskCreateForm(forms.ModelForm):
    """
    Task creation form by user
    """

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'priority', 'due_date')
        widgets = {
            'due_date': DateTimeInput(),
        }


class UserWorkerCreateForm(forms.ModelForm):
    """
    Worker create form by user
    """

    class Meta:
        model = Worker
        fields = ('user', 'role', 'price_per_hour', 'skills', 'status', 'availability_date')
        widgets = {
            'availability_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.exclude(worker__isnull=False)


class UserVehicleCreateForm(forms.ModelForm):
    """
    Vehicle create form by user
    """

    class Meta:
        model = Vehicle
        fields = ('license_plate', 'car_model', 'car_make', 'capacity', 'picture')


class TaskForm(forms.ModelForm):
    """
    Task form
    """

    class Meta:
        model = Task
        fields = '__all__'


class AddWorkerForm(forms.Form):
    """
    Addition worker adding fform
    """
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(), empty_label=None)


class TaskReviewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'content',)


WorkerGroupFormSet = inlineformset_factory(Worker, WorkerGroup, form=WorkerGroupForm, extra=2, can_delete=True)
WorkerTaskFormset = inlineformset_factory(Worker, WorkerTask, form=WorkerTaskForm, extra=2, can_delete=True)
TaskProjectFormSet = inlineformset_factory(Project, ProjectTask, form=ProjectTaskForm, extra=2, can_delete=True)
