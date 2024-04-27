#unittest start ------

# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Task, Priority
# from django.utils import timezone

# class TaskListViewTestCase(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='password123')

#         # Create a test priority
#         priority = Priority.objects.create(name='High')

#         # Create a test task with the priority
#         self.task1 = Task.objects.create(
#             description='Task 1',
#             assigned_user=self.user,
#             deadline=timezone.now(),
#             priority=priority  # Pass the created priority object
#         )

#         # Log in the test user
#         self.client = Client()
#         self.client.login(username='testuser', password='password123')

#         # Create another task for user
#         self.task2 = Task.objects.create(description='Task 2', assigned_user=self.user, deadline=timezone.now(), priority=priority)

#     def test_task_list_view(self):
#         # Get the task list view URL
#         url = reverse('task_list')

#         # Make a GET request to the task list view
#         response = self.client.get(url)

#         # Check that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, 200)

#         # Check that the tasks are present in the response context
#         self.assertIn('tasks', response.context)

#         # Check that the tasks returned in the response context match the tasks created in the setUp method
#         tasks = response.context['tasks']
#         self.assertEqual(len(tasks), 2)
#         self.assertEqual(tasks[0].description, 'Task 1')
#         self.assertEqual(tasks[1].description, 'Task 2')

#unittest end ------

#integration start ------

from django.urls import reverse
from rest_framework.test import APITestCase
from datetime import datetime
from django.contrib.auth import get_user_model
from .models import Task, Priority

User = get_user_model()

class TaskIntegrationTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")  # Create user with password

        # Create a test priority
        self.priority = Priority.objects.create(name="High")

    def test_task_flow(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Create a task with primary key values for assigned_user and priority
        task_data = {
            'description': 'Test task',
            'assigned_user': self.user.id,  # Primary key value for assigned_user
            'deadline': datetime.now(),
            'priority': self.priority.id  # Primary key value for priority
        }

        # Make a POST request to create the task
        response = self.client.post(reverse('task_list_create'), task_data, format='json')

        # Print the response content
        print("POST Response Content:", response.content)

        # Check if the task was created successfully
        self.assertEqual(response.status_code, 201)  # HTTP 201 Created
        self.assertEqual(Task.objects.count(), 1)
        print("Task count:", Task.objects.count())

        # Retrieve the created task from the database
        task = Task.objects.first()

        # Check if the retrieved task matches the created task
        self.assertEqual(task.description, "Test task")
        self.assertEqual(task.assigned_user, self.user)
        self.assertIsNotNone(task.deadline)
        self.assertEqual(task.priority, self.priority)

        # Retrieve the task using its detail endpoint
        detail_response = self.client.get(reverse('task_detail_view', kwargs={'pk': task.id}))

        # Print the detail response content
        print("Detail Response Content:", detail_response.content)

        # Check if the task detail endpoint returns the expected data
        self.assertEqual(detail_response.status_code, 200)  # HTTP 200 OK
        self.assertEqual(detail_response.data['description'], "Test task")

#integration end ------