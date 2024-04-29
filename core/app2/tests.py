from datetime import datetime, timedelta, timezone
from django.test import TestCase
from app1.models import Task, Priority
from app2.domain.model import TaskDomain
from app2.services.commands import AddTaskCommand, ListTasksCommand, DeleteTaskCommand, EditTaskCommand
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

        # Check if the task already exists in the database
        existing_task = Task.objects.filter(description='Sample Task').first()
        if not existing_task:
            # Create the sample task for testing delete and edit commands if it doesn't exist
            Task.objects.create(
                id=self.task_data.id,
                description=self.task_data.description,
                assigned_user=self.user,
                deadline=self.task_data.deadline,
                priority=priority,
            )

    def test_command_add(self):
        # Test AddTaskCommand
        add_command = AddTaskCommand()
        add_command.execute(self.task_data)

        # Check if the task was added successfully
        self.assertEqual(Task.objects.count(), 2)

        # Check if the added task has the correct details
        added_task = Task.objects.first()
        self.assertEqual(added_task.description, 'Sample Task')
        self.assertEqual(added_task.assigned_user, self.user)

    def test_command_list(self):
        # Test ListTasksCommand
        list_command = ListTasksCommand()
        tasks = list_command.execute()

        # Check if the list contains the added task
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, 'Sample Task')
        self.assertEqual(tasks[0].assigned_user, self.user)

    def test_command_delete(self):
        # Test DeleteTaskCommand
        delete_command = DeleteTaskCommand()
        delete_command.execute({'id': self.task_data.id})

        # Check if the task was deleted successfully
        self.assertEqual(Task.objects.count(), 0)

    def test_command_edit(self):
        # Test EditTaskCommand
        new_description = 'Updated Task Description'
        new_deadline = datetime.now(timezone.utc)  # Assuming new deadline in UTC
        new_priority = Priority.objects.create(name='Low')  # Assuming new priority
        edit_data = {
            'id': self.task_data.id,
            'description': new_description,
            'assigned_user': self.user,
            'deadline': new_deadline,
            'priority': new_priority,
        }

        edit_command = EditTaskCommand()
        edit_command.execute(edit_data)

        # Refresh the task instance from the database
        edited_task = Task.objects.get(id=self.task_data.id)

        # Check if the task was edited successfully
        self.assertEqual(edited_task.description, new_description)
        self.assertEqual(edited_task.assigned_user, self.user)
        self.assertEqual(edited_task.priority, new_priority)

        # Assert that the deadline matches approximately
        self.assertAlmostEqual(edited_task.deadline, new_deadline, delta=timedelta(seconds=1))
