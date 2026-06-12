import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from models import User, Project, Task


class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        Path(data_dir).mkdir(exist_ok=True)
        
        if not os.path.exists(self.users_file):
            self._save_users({})

    def _load_users_raw(self) -> dict:
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted user data file: {e}")

    def _save_users(self, users_data: dict):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to persist user data: {e}")

    def add_user(self, user: User) -> bool:
        users_data = self._load_users_raw()
        if user.user_id in users_data:
            return False
        users_data[user.user_id] = user.to_dict()
        self._save_users(users_data)
        return True

    def get_user(self, user_id: str) -> Optional[User]:
        users_data = self._load_users_raw()
        if user_id not in users_data:
            return None
        return User.from_dict(users_data[user_id])

    def get_user_by_name(self, name: str) -> Optional[User]:
        for user_data in self._load_users_raw().values():
            if user_data["name"].lower() == name.lower():
                return User.from_dict(user_data)
        return None

    def list_users(self) -> List[User]:
        return [User.from_dict(data) for data in self._load_users_raw().values()]

    def update_user(self, user: User) -> bool:
        users_data = self._load_users_raw()
        if user.user_id not in users_data:
            return False
        users_data[user.user_id] = user.to_dict()
        self._save_users(users_data)
        return True

    def delete_user(self, user_id: str) -> bool:
        users_data = self._load_users_raw()
        if user_id not in users_data:
            return False
        del users_data[user_id]
        self._save_users(users_data)
        return True

    def add_project_to_user(self, user_id: str, project: Project) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        user.add_project(project)
        return self.update_user(user)

    def get_project_by_name(self, project_name: str) -> Optional[Tuple[str, Project]]:
        for user in self.list_users():
            for project in user.projects:
                if project.title.lower() == project_name.lower():
                    return (user.user_id, project)
        return None

    def add_task_to_project(self, user_id: str, project_id: str, task: Task) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        project = user.get_project(project_id)
        if not project:
            return False
        project.add_task(task)
        return self.update_user(user)

    def update_task_status(self, user_id: str, project_id: str, task_id: str, 
                          completed: bool) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        project = user.get_project(project_id)
        if not project:
            return False
        task = project.get_task(task_id)
        if not task:
            return False
        
        task.mark_complete() if completed else task.mark_incomplete()
        return self.update_user(user)

    def export_all_data(self) -> dict:
        return {"users": self._load_users_raw()}
