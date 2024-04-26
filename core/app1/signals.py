from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task

# Define a signal handler to execute when a new task is created
@receiver(post_save, sender=Task)
def task_created(sender, instance, created, **kwargs):
    if created:
        # Perform some action when a new task is created, e.g., send a notification
        print(f"A new task '{instance.description}' has been created!")