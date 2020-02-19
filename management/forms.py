from django import forms

from .models import TaskSubmit, runSubmit

class TaskSubmitForm(forms.ModelForm):
    class Meta:
        model = TaskSubmit
        fields = ('title', 'img', 'description', 'dataset', 'category')

class RunSubmitForm(forms.ModelForm):
    class Meta:
        model = runSubmit
        fields = ('img', 'gpu', 'ind', 'dataset', 'retrycount','title', 'description', 'model') #