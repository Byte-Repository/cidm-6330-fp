"""
This module utilizes the command pattern to specify and implement the business logic layer for task management.
"""
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from injector import inject, Injector

import requests
from django.db import transaction

from app1.models import Task 
from app2.domain.model import TaskDomain


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        """
        Method to execute the command with provided data.
        """
        pass


class InjectorConfig:
    @inject
    def __init__(self):
        self.injector = Injector()

    def get_injector(self):
        return self.injector


class AddTaskCommand(Command):
    """
    Command to add a new task.
    """

    @inject
    @transaction.atomic
    def execute(self, data, injector: Injector = None):
        """
        Execute method to add a new task.
        """
        now = datetime.now()
        task = Task(description=data.description, assigned_user=data.assigned_user, deadline=data.deadline, priority=data.priority, created_at=now)
        task.save()

class ListTasksCommand(Command):
    """
    Command to list all tasks.
    """

    @inject
    def __init__(self, injector: Injector = None):
        self.injector = injector

    def execute(self):
        """
        Execute method to list all tasks.
        """
        return Task.objects.all()


class DeleteTaskCommand(Command):
    """
    Command to delete a task.
    """

    @inject
    @transaction.atomic
    def execute(self, data, injector: Injector = None):
        """
        Execute method to delete a task.
        """
        task = Task.objects.get(id=data['id'])
        task.delete()


class EditTaskCommand(Command):
    """
    Command to edit a task.
    """

    @inject
    @transaction.atomic
    def execute(self, data, injector: Injector = None):
        """
        Execute method to edit a task.
        """
        task = Task.objects.get(id=data['id'])
        task.description = data['description']
        task.assigned_user = data['assigned_user']
        task.deadline = data['deadline']
        task.priority = data['priority']
        task.save()
