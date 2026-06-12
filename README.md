# Project Management CLI

A command-line tool for managing users, projects, and tasks with persistent JSON storage.

## Quick Start

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/project-management-cli.git
cd project-management-cli
```

### Setup

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### User Commands

Add a user:
```bash
python3 index.py user add --name "Alice" --email "alice@example.com" --role "admin"
```

List all users:
```bash
python3 index.py user list
```

View user details:
```bash
python3 index.py user view --name "Alice"
```

Delete a user:
```bash
python3 index.py user delete --name "Alice"
```

### Project Commands

Add a project:
```bash
python3 index.py project add --user "Alice" --title "My Project" --description "Project description"
```

List user projects:
```bash
python3 index.py project list --user "Alice"
```

View project details:
```bash
python3 index.py project view --name "My Project"
```

Delete a project:
```bash
python3 index.py project delete --user "Alice" --name "My Project"
```

### Task Commands

Add a task:
```bash
python3 index.py task add --project "My Project" --title "Task 1" --description "Do something" --assigned-to "Bob"
```

List project tasks:
```bash
python3 index.py task list --project "My Project"
```

Complete a task:
```bash
python3 index.py task complete --project "My Project" --title "Task 1"
```

Mark task incomplete:
```bash
python3 index.py task incomplete --project "My Project" --title "Task 1"
```

Delete a task:
```bash
python3 index.py task delete --project "My Project" --title "Task 1"
```

## Architecture

- **index.py** - Main entry point
- **cli.py** - Command-line interface with argparse
- **models.py** - User, Project, and Task classes
- **data_manager.py** - JSON persistence layer
- **tests.py** - Unit tests
- **data/** - JSON storage directory

## Data Storage

All data is persisted in `data/users.json` in JSON format with the following hierarchy:
- Users
  - Projects (owned by each user)
    - Tasks (contained in each project)

## Testing

Run the test suite:
```bash
python3 tests.py
```

## Requirements

See `requirements.txt` for dependencies. Currently uses:
- **tabulate** - For formatted table output in the CLI
