from django import forms
from django.forms.models import inlineformset_factory
from .models import *


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class WorkerGroupForm(forms.ModelForm):
    class Meta:
        model = WorkerGroup
        fields = ('project', 'vehicle', 'worker')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worker'].queryset = Worker.objects.exclude(workergroup__isnull=False)
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(workergroup__isnull=False)


class WorkerTaskForm(forms.ModelForm):
    class Meta:
        model = WorkerTask
        fields = ('task',)


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ('project',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'place_city', 'customer', 'project_start', 'project_end']
        widgets = {
            'project_start': DateInput(),
            'project_end': DateInput(),
        }


class UserTaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'priority', 'due_date')
        widgets = {
            'due_date': DateTimeInput(),
        }


class UserWorkerCreateForm(forms.ModelForm):
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
    class Meta:
        model = Vehicle
        fields = ('license_plate', 'car_model', 'car_make', 'capacity')


WorkerGroupFormSet = inlineformset_factory(Worker, WorkerGroup, form=WorkerGroupForm, extra=2, can_delete=True)
WorkerTaskFormset = inlineformset_factory(Worker, WorkerTask, form=WorkerTaskForm, extra=2, can_delete=True)
TaskProjectFormSet = inlineformset_factory(Project, ProjectTask, form=ProjectTaskForm, extra=2, can_delete=True)
