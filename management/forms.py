from django import forms

from .models import TaskSubmit, runSubmit

class TaskSubmitForm(forms.ModelForm):
    class Meta:
        model = TaskSubmit
        fields = ('title', 'img', 'description', 'dataset', 'category')

class RunSubmitForm(forms.ModelForm):
    class Meta:
        model = runSubmit
        fields = ('title', 'description', 'dataset', 'model', 'img', 'gpu', 'ind', 'retrycount')#