from django.contrib.auth.models import User
from django.db import models
from api.models.choices import Status


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    title = models.CharField(default='Undefined', max_length=64)
    description = models.CharField(default='No description.', max_length=1024)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    deadline = models.DateField(null=True)
    status = models.TextField(choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return str(self.title)
