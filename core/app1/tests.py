#unittest start ------

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Priority
from django.utils import timezone

class TaskListViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Create a test priority
        priority = Priority.objects.create(name='High')

        # Create a test task with the priority
        self.task1 = Task.objects.create(
            description='Task 1',
            assigned_user=self.user,
            deadline=timezone.now(),
            priority=priority  # Pass the created priority object
        )

        # Log in the test user
        self.client = Client()
        self.client.login(username='testuser', password='password123')

        # Create another task for user
        self.task2 = Task.objects.create(description='Task 2', assigned_user=self.user, deadline=timezone.now(), priority=priority)

    def test_task_list_view(self):
        # Get the task list view URL
        url = reverse('task_list')

        # Make a GET request to the task list view
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the tasks are present in the response context
        self.assertIn('tasks', response.context)

        # Check that the tasks returned in the response context match the tasks created in the setUp method
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, 'Task 1')
        self.assertEqual(tasks[1].description, 'Task 2')

#unittest end ------

#integration start ------

from django.test import TestCase
from datetime import datetime
from django.contrib.auth.models import User
from .models import Task, Priority

class TaskIntegrationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(username="testuser")

        # Create a test priority
        self.priority = Priority.objects.create(name="High")

    def test_task_flow(self):
        # Create a task
        task = Task(
            description="Test task",
            assigned_user=self.user,
            deadline=datetime.now(),
            priority=self.priority
        )

        # Save the task to the database
        task.save()

        # Retrieve the task from the database
        retrieved_task = Task.objects.get(description="Test task")

        # Check if the retrieved task matches the created task
        self.assertEqual(retrieved_task.description, "Test task")
        self.assertEqual(retrieved_task.assigned_user, self.user)
        self.assertIsNotNone(retrieved_task.deadline)
        self.assertEqual(retrieved_task.priority, self.priority)


#integration end ------