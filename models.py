from datetime import datetime
from typing import List, Optional


class Task:
    def __init__(self, task_id: str, title: str, description: str = "", 
                 completed: bool = False, assigned_to: Optional[str] = None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = completed
        self.assigned_to = assigned_to
        self.created_at = datetime.now().isoformat()

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            assigned_to=data.get("assigned_to")
        )
        task.created_at = data.get("created_at", task.created_at)
        return task


class Project:
    def __init__(self, project_id: str, title: str, description: str = "", 
                 owner: str = ""):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.owner = owner
        self.tasks: List[Task] = []
        self.created_at = datetime.now().isoformat()

    def add_task(self, task: Task):
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_completion_percentage(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.completed)
        return (completed / len(self.tasks)) * 100

    def to_dict(self) -> dict:
        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "tasks": [t.to_dict() for t in self.tasks],
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(
            project_id=data["project_id"],
            title=data["title"],
            description=data.get("description", ""),
            owner=data.get("owner", "")
        )
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        project.created_at = data.get("created_at", project.created_at)
        return project


class User:
    def __init__(self, user_id: str, name: str, email: str = "", role: str = "user"):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.projects: List[Project] = []
        self.created_at = datetime.now().isoformat()

    def add_project(self, project: Project):
        project.owner = self.user_id
        if project not in self.projects:
            self.projects.append(project)

    def remove_project(self, project_id: str) -> bool:
        self.projects = [p for p in self.projects if p.project_id != project_id]
        return True

    def get_project(self, project_id: str) -> Optional[Project]:
        for project in self.projects:
            if project.project_id == project_id:
                return project
        return None

    def list_projects(self) -> List[Project]:
        return self.projects

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "projects": [p.to_dict() for p in self.projects],
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(
            user_id=data["user_id"],
            name=data["name"],
            email=data.get("email", ""),
            role=data.get("role", "user")
        )
        user.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        user.created_at = data.get("created_at", user.created_at)
        return user
