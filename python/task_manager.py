from typing import List, Dict

class TaskManager:
    def __init__(self):
        self.tasks: List[Dict[str, str]] = []

    def add_task(self, description: str) -> str:
        task_id = len(self.tasks) + 1
        self.tasks.append({"id": task_id, "description": description, "status": "pending"})
        return f"Task {task_id} added: {description}"

    def list_tasks(self) -> str:
        if not self.tasks:
            return "No tasks found."
        return "\n".join([f"{task['id']}. [{task['status']}] {task['description']}" for task in self.tasks])

    def complete_task(self, task_id: int) -> str:
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = "completed"
                return f"Task {task_id} marked as completed."
        return f"Task {task_id} not found."

    def remove_task(self, task_id: int) -> str:
        for task in self.tasks:
            if task['id'] == task_id:
                self.tasks.remove(task)
                return f"Task {task_id} removed."
        return f"Task {task_id} not found."

    def handle_command(self, command: str) -> str:
        parts = command.split()
        if parts[0] == "add":
            return self.add_task(" ".join(parts[1:]))
        elif parts[0] == "list":
            return self.list_tasks()
        elif parts[0] == "complete":
            return self.complete_task(int(parts[1]))
        elif parts[0] == "remove":
            return self.remove_task(int(parts[1]))
        else:
            return "Invalid task command. Use 'add', 'list', 'complete', or 'remove'."