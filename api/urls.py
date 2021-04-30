from django.urls import path

from api.views import *

urlpatterns = [
    path('tasks/', task_list, name='read'),
    path('task/<str:pk>/', task_item, name='item'),
]
