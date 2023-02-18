from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Task(models.Model):
    name=models.CharField(max_length=250)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    date=models.DateField()
    updated=models.DateTimeField(auto_now=True)
    finished=models.BooleanField(default=False)
    def __str__(self):
        return self.name