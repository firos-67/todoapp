from django.contrib.auth.models import User
from django.forms import TextInput, DateInput

from .models import Task
from django import forms


class TodoForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['name','date']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control mt-3'}),
            'date': DateInput(attrs={'class': 'form-control',}),
        }
        labels={
            'name':'',
            'date':''
        }


