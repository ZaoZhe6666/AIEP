from django import forms

from .models import TaskSubmit, runSubmit, Datasets, Comment, Forum

class TaskSubmitForm(forms.ModelForm):
    class Meta:
        model = TaskSubmit
        fields = ('title', 'img', 'description', 'startTime', 'endTime', 'algorithm', 'modelType', 'ind', 'tags', 'dataset')


class RunSubmitForm(forms.ModelForm):
    class Meta:
        model = runSubmit
        fields = ('title', 'description', 'dataset', 'evaluate_method', 'model', 'model_data')

class TaskInnerSubmitForm(forms.ModelForm):
    class Meta:
        model = runSubmit
        fields = ('model', )

class DatasetSubmitForm(forms.ModelForm):
    class Meta:
        model = Datasets
        fields = ('name', 'description', 'specifications', 'dataType', 'public', 'datasets')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

class ForumSubmitForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ('title', 'content', 'tags')