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
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Task, Priority

class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.priority = Priority.objects.create(name='High')

    def test_create_task(self):
        """
        Test creating a task via the API endpoint.
        """
        url = reverse('task_list')
        data = {
            'description': 'Test Task',
            'assigned_user': self.user.id,
            'deadline': '2024-04-30T12:00:00Z',
            'priority': self.priority.id,
        }
        
        # Log in the user
        self.client.force_login(self.user)

        # Send a POST request to the create endpoint with the data
        response = self.client.post(url, data, format='json')

        # Assert that the response status code is HTTP 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that a Task object was created in the database
        self.assertEqual(Task.objects.count(), 1)

        # Assert that the description of the created task matches the description sent in the request
        self.assertEqual(Task.objects.get().description, 'Test Task')

#integration end ------