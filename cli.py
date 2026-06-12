import argparse
import uuid
from typing import Optional, Tuple

from tabulate import tabulate

from models import User, Project, Task
from data_manager import DataManager


class ProjectManagerCLI:
    def __init__(self, data_dir: str = "data"):
        self.dm = DataManager(data_dir)

    def _find_task(self, project: Project, task_name: str) -> Optional[Task]:
        """Locate a task by case-insensitive name match."""
        for task in project.tasks:
            if task.title.lower() == task_name.lower():
                return task
        return None

    def _find_project_item(self, user: User, project_name: str) -> Optional[Project]:
        """Locate a project by case-insensitive name match."""
        for proj in user.projects:
            if proj.title.lower() == project_name.lower():
                return proj
        return None

    def _truncate(self, text: str, length: int = 30) -> str:
        """Truncate text with ellipsis."""
        return text[:length] + "..." if len(text) > length else text

    def add_user(self, name: str, email: str = "", role: str = "user") -> bool:
        user = User(str(uuid.uuid4())[:8], name, email, role)
        if not self.dm.add_user(user):
            print(f"Error: User '{name}' already exists or could not be added")
            return False
        print(f"Added user '{name}'")
        return True

    def list_users(self) -> bool:
        users = self.dm.list_users()
        if not users:
            print("No users found")
            return True

        rows = [
            [u.user_id, u.name, u.email, u.role, len(u.projects)]
            for u in users
        ]
        print("\n" + tabulate(rows, headers=["ID", "Name", "Email", "Role", "Projects"], tablefmt="grid") + "\n")
        return True

    def view_user(self, user_name: str) -> bool:
        user = self.dm.get_user_by_name(user_name)
        if not user:
            print(f"User '{user_name}' not found")
            return False
        print(f"\nUser: {user.name}")
        print(f"Email: {user.email or '(none)'}")
        print(f"Role: {user.role}")
        print(f"Projects: {len(user.projects)}\n")
        return True

    def delete_user(self, user_name: str) -> bool:
        user = self.dm.get_user_by_name(user_name)
        if not user:
            print(f"User '{user_name}' not found")
            return False
        self.dm.delete_user(user.user_id)
        print(f"Deleted user '{user_name}'")
        return True

    def add_project(self, user_name: str, title: str, description: str = "") -> bool:
        user = self.dm.get_user_by_name(user_name)
        if not user:
            print(f"User '{user_name}' not found")
            return False

        project = Project(str(uuid.uuid4())[:8], title, description, user.user_id)
        user.add_project(project)
        if not self.dm.update_user(user):
            print(f"Failed to add project '{title}'")
            return False
        print(f"Added project '{title}'")
        return True

    def list_user_projects(self, user_name: str) -> bool:
        user = self.dm.get_user_by_name(user_name)
        if not user:
            print(f"User '{user_name}' not found")
            return False

        if not user.projects:
            print(f"No projects for '{user_name}'")
            return True

        rows = [
            [p.project_id, p.title, len(p.tasks), f"{p.get_completion_percentage():.0f}%", self._truncate(p.description)]
            for p in user.projects
        ]
        print(f"\nProjects for {user_name}:\n")
        print(tabulate(rows, headers=["ID", "Title", "Tasks", "Progress", "Description"], tablefmt="grid") + "\n")
        return True

    def view_project(self, project_name: str) -> bool:
        result = self.dm.get_project_by_name(project_name)
        if not result:
            print(f"Project '{project_name}' not found")
            return False

        user_id, project = result
        user = self.dm.get_user(user_id)
        print(f"\nProject: {project.title}")
        print(f"Owner: {user.name}")
        print(f"Description: {project.description or '(none)'}")
        print(f"Progress: {project.get_completion_percentage():.0f}%")
        print(f"Tasks: {len(project.tasks)}\n")
        return True

    def delete_project(self, user_name: str, project_name: str) -> bool:
        user = self.dm.get_user_by_name(user_name)
        if not user:
            print(f"User '{user_name}' not found")
            return False

        project = self._find_project_item(user, project_name)
        if not project:
            print(f"Project '{project_name}' not found")
            return False

        user.remove_project(project.project_id)
        self.dm.update_user(user)
        print(f"Deleted project '{project_name}'")
        return True

    def add_task(self, project_name: str, title: str, description: str = "",
                 assigned_to: Optional[str] = None) -> bool:
        result = self.dm.get_project_by_name(project_name)
        if not result:
            print(f"Project '{project_name}' not found")
            return False

        user_id, project = result
        task = Task(str(uuid.uuid4())[:8], title, description, assigned_to=assigned_to)
        project.add_task(task)
        if not self.dm.add_task_to_project(user_id, project.project_id, task):
            print(f"Failed to add task '{title}'")
            return False
        print(f"Added task '{title}'")
        return True

    def list_project_tasks(self, project_name: str) -> bool:
        result = self.dm.get_project_by_name(project_name)
        if not result:
            print(f"Project '{project_name}' not found")
            return False

        user_id, project = result
        if not project.tasks:
            print(f"No tasks in '{project_name}'")
            return True

        rows = [
            [t.task_id, t.title, "Done" if t.completed else "Pending", t.assigned_to or "—", self._truncate(t.description)]
            for t in project.tasks
        ]
        print(f"\nTasks in '{project_name}':\n")
        print(tabulate(rows, headers=["ID", "Title", "Status", "Assigned", "Description"], tablefmt="grid") + "\n")
        return True

    def complete_task(self, project_name: str, task_name: str) -> bool:
        return self._update_task_completion(project_name, task_name, True)

    def incomplete_task(self, project_name: str, task_name: str) -> bool:
        return self._update_task_completion(project_name, task_name, False)

    def _update_task_completion(self, project_name: str, task_name: str, completed: bool) -> bool:
        result = self.dm.get_project_by_name(project_name)
        if not result:
            print(f"Project '{project_name}' not found")
            return False

        user_id, project = result
        task = self._find_task(project, task_name)
        if not task:
            print(f"Task '{task_name}' not found")
            return False

        self.dm.update_task_status(user_id, project.project_id, task.task_id, completed)
        status = "done" if completed else "pending"
        print(f"Task '{task_name}' marked {status}")
        return True

    def delete_task(self, project_name: str, task_name: str) -> bool:
        result = self.dm.get_project_by_name(project_name)
        if not result:
            print(f"Project '{project_name}' not found")
            return False

        user_id, project = result
        task = self._find_task(project, task_name)
        if not task:
            print(f"Task '{task_name}' not found")
            return False

        project.remove_task(task.task_id)
        user = self.dm.get_user(user_id)
        for p in user.projects:
            if p.project_id == project.project_id:
                p.tasks = project.tasks
                break
        self.dm.update_user(user)
        print(f"Deleted task '{task_name}'")
        return True


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='project-manager', description='Project Management CLI')
    subparsers = parser.add_subparsers(dest='command')

    user = subparsers.add_parser('user', help='User commands')
    user_sub = user.add_subparsers(dest='user_command')
    
    add_u = user_sub.add_parser('add', help='Add user')
    add_u.add_argument('--name', required=True)
    add_u.add_argument('--email', default='')
    add_u.add_argument('--role', default='user')
    user_sub.add_parser('list', help='List all users')
    
    view_u = user_sub.add_parser('view', help='View user')
    view_u.add_argument('--name', required=True)
    
    del_u = user_sub.add_parser('delete', help='Delete user')
    del_u.add_argument('--name', required=True)

    proj = subparsers.add_parser('project', help='Project commands')
    proj_sub = proj.add_subparsers(dest='project_command')
    
    add_p = proj_sub.add_parser('add', help='Add project')
    add_p.add_argument('--user', required=True)
    add_p.add_argument('--title', required=True)
    add_p.add_argument('--description', default='')
    
    list_p = proj_sub.add_parser('list', help='List projects')
    list_p.add_argument('--user', required=True)
    
    view_p = proj_sub.add_parser('view', help='View project')
    view_p.add_argument('--name', required=True)
    
    del_p = proj_sub.add_parser('delete', help='Delete project')
    del_p.add_argument('--user', required=True)
    del_p.add_argument('--name', required=True)

    task = subparsers.add_parser('task', help='Task commands')
    task_sub = task.add_subparsers(dest='task_command')
    
    add_t = task_sub.add_parser('add', help='Add task')
    add_t.add_argument('--project', required=True)
    add_t.add_argument('--title', required=True)
    add_t.add_argument('--description', default='')
    add_t.add_argument('--assigned-to', default=None)
    
    list_t = task_sub.add_parser('list', help='List tasks')
    list_t.add_argument('--project', required=True)
    
    comp_t = task_sub.add_parser('complete', help='Mark task done')
    comp_t.add_argument('--project', required=True)
    comp_t.add_argument('--title', required=True)
    
    incomp_t = task_sub.add_parser('incomplete', help='Mark task pending')
    incomp_t.add_argument('--project', required=True)
    incomp_t.add_argument('--title', required=True)
    
    del_t = task_sub.add_parser('delete', help='Delete task')
    del_t.add_argument('--project', required=True)
    del_t.add_argument('--title', required=True)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = ProjectManagerCLI()

    if args.command == 'user':
        if args.user_command == 'add':
            cli.add_user(args.name, args.email, args.role)
        elif args.user_command == 'list':
            cli.list_users()
        elif args.user_command == 'view':
            cli.view_user(args.name)
        elif args.user_command == 'delete':
            cli.delete_user(args.name)
    elif args.command == 'project':
        if args.project_command == 'add':
            cli.add_project(args.user, args.title, args.description)
        elif args.project_command == 'list':
            cli.list_user_projects(args.user)
        elif args.project_command == 'view':
            cli.view_project(args.name)
        elif args.project_command == 'delete':
            cli.delete_project(args.user, args.name)
    elif args.command == 'task':
        if args.task_command == 'add':
            cli.add_task(args.project, args.title, args.description, args.assigned_to)
        elif args.task_command == 'list':
            cli.list_project_tasks(args.project)
        elif args.task_command == 'complete':
            cli.complete_task(args.project, args.title)
        elif args.task_command == 'incomplete':
            cli.incomplete_task(args.project, args.title)
        elif args.task_command == 'delete':
            cli.delete_task(args.project, args.title)


if __name__ == '__main__':
    main()
