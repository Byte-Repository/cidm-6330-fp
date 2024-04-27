from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from app1.models import Task
from app1.models import Priority
from app2.domain.model import TaskDomain
from app2.services.commands import AddTaskCommand


from django.contrib.auth.models import User

class TestCommands(TestCase):
    def setUp(self):
        # Create a User instance for testing
        self.user = User.objects.create(username='john_doe')

        # Create a Priority instance for testing
        priority = Priority.objects.create(name='High')

        # Sample task data
        self.task_data = TaskDomain(
            id=3,
            description='Sample Task',
            assigned_user=self.user,
            deadline=datetime.now(),
            priority=priority,  # Assign the Priority instance here
        )

    def test_command_add(self):
        add_command = AddTaskCommand()
        add_command.execute(self.task_data)

        # Check if the task was added successfully
        self.assertEqual(Task.objects.count(), 1)

        # Check if the added task has the correct details
        added_task = Task.objects.first()
        self.assertEqual(added_task.description, 'Sample Task')
        self.assertEqual(added_task.assigned_user, self.user)
