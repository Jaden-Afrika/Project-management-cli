import unittest
import tempfile
import shutil

from models import User, Project, Task
from data_manager import DataManager
from cli import ProjectManagerCLI


class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User("u1", "Alice", "alice@example.com", "admin")
        self.assertEqual(user.user_id, "u1")
        self.assertEqual(user.name, "Alice")

    def test_add_project(self):
        user = User("u1", "Alice")
        project = Project("p1", "Project 1")
        user.add_project(project)
        self.assertEqual(len(user.projects), 1)


class TestProjectModel(unittest.TestCase):
    def test_project_creation(self):
        project = Project("p1", "CLI Tool", "Build CLI", "user1")
        self.assertEqual(project.project_id, "p1")
        self.assertEqual(project.title, "CLI Tool")

    def test_add_task(self):
        project = Project("p1", "Project")
        task = Task("t1", "Task 1")
        project.add_task(task)
        self.assertEqual(len(project.tasks), 1)

    def test_completion_percentage(self):
        project = Project("p1", "Project")
        task1 = Task("t1", "Task 1")
        task2 = Task("t2", "Task 2")
        project.add_task(task1)
        project.add_task(task2)
        task1.mark_complete()
        self.assertEqual(project.get_completion_percentage(), 50.0)


class TestTaskModel(unittest.TestCase):
    def test_task_creation(self):
        task = Task("t1", "Feature", "Add button")
        self.assertEqual(task.task_id, "t1")
        self.assertFalse(task.completed)

    def test_mark_complete(self):
        task = Task("t1", "Task")
        task.mark_complete()
        self.assertTrue(task.completed)


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.dm = DataManager(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_user(self):
        user = User("u1", "Alice")
        self.assertTrue(self.dm.add_user(user))

    def test_get_user(self):
        user = User("u1", "Alice")
        self.dm.add_user(user)
        retrieved = self.dm.get_user("u1")
        self.assertIsNotNone(retrieved)

    def test_list_users(self):
        user1 = User("u1", "Alice")
        user2 = User("u2", "Bob")
        self.dm.add_user(user1)
        self.dm.add_user(user2)
        self.assertEqual(len(self.dm.list_users()), 2)

    def test_delete_user(self):
        user = User("u1", "Alice")
        self.dm.add_user(user)
        self.dm.delete_user("u1")
        self.assertIsNone(self.dm.get_user("u1"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
