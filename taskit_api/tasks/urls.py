""" Contains route definitions for the Todo Views """
from django.urls import path
from tasks.views import (ListCreateTasksView, RetrieveUpdateDestroyTaskView)

urlpatterns = [
    path('', ListCreateTasksView.as_view(), name='tasks'),
    path('<str:id>/', RetrieveUpdateDestroyTaskView.as_view(), name='task'),
]
