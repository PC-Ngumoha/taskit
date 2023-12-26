""" Contains model field definitions for the task model """
from authentication.models import User
from common.models import BaseModel
from django.db import models


class Task(BaseModel):
    title = models.CharField(max_length=255)
    details = models.TextField()
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
