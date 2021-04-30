from django.db import models


class Status(models.TextChoices):
    NEW = 'New'
    PLANNED = 'Planned'
    IN_PROGRESS = 'In progress'
    COMPLETED = 'Completed'
