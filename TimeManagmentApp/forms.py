from django import forms
from .models import *


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture',)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class WorkerAssignmentForm(forms.ModelForm):
    class Meta:
        model = WorkerGroup
        fields = ('project_id.name',)