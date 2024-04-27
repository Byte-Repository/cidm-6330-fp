class TaskDomain:
    """
    Task domain model.
    """

    def __init__(self, id, description, assigned_user, deadline, priority):
        """
        Initialize a Task object with the provided attributes.
        
        Args:
            id (int): The unique identifier of the task.
            description (str): The description of the task.
            assigned_user (str): The user assigned to the task.
            deadline (date): The deadline for completing the task.
            priority (str): The priority level of the task.
        """
        self.id = id
        self.description = description
        self.assigned_user = assigned_user
        self.deadline = deadline
        self.priority = priority

    def __str__(self):
        """
        Return a string representation of the task.
        """
        return f"{self.description}"
