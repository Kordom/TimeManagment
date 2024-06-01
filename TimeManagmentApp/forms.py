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
        fields = ('project', 'vehicle',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['project'].queryset = Project.objects.all()


class WorkerTaskForm(forms.ModelForm):
    class Meta:
        model = WorkerTask
        fields = ('task', 'worker')


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ('project',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'place_city', 'customer']


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class DateInput(forms.DateInput):
    input_type = 'date'


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


WorkerGroupFormSet = inlineformset_factory(Worker, WorkerGroup, form=WorkerGroupForm, extra=2, can_delete=True)
WorkerTaskFormset = inlineformset_factory(Worker, WorkerTask, form=WorkerTaskForm, extra=2, can_delete=True)
TaskProjectFormSet = inlineformset_factory(Project, ProjectTask, form=ProjectTaskForm, extra=2, can_delete=True)
