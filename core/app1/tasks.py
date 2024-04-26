from celery import shared_task
from .models import Task

@shared_task
def process_task(task_id):
    # Fetch the task object from the database
    task = Task.objects.get(id=task_id)
    
    # Perform some processing on the task
    # For example, you could send an email notification, update the task status, etc.
    
    # Here's a placeholder example of updating the task status
    task.status = 'completed'
    task.save()

    # You can return some result if needed
    return {'task_id': task_id, 'status': 'completed'}
