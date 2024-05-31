from django import forms
from django.forms.models import inlineformset_factory
from .models import *


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


class WorkerTaskForm(forms.ModelForm):
    class Meta:
        model = WorkerTask
        fields = ('task', 'worker')


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ('task', 'project')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'place_city', 'customer']


class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class UserTaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'priority', 'due_date')
        widgets = {
            'due_date': DateInput(),
        }


WorkerGroupFormSet = inlineformset_factory(Worker, WorkerGroup, form=WorkerGroupForm, extra=2, can_delete=True)
WorkerTaskFormset = inlineformset_factory(Worker, WorkerTask, form=WorkerTaskForm, extra=2, can_delete=True)
TaskProjectFormSet = inlineformset_factory(Project, ProjectTask, form=ProjectTaskForm, extra=2, can_delete=True)
